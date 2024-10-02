-- Assuming you have a users table and a projects table structured as follows:
-- users(id INT, name VARCHAR(255))
-- projects(id INT, name VARCHAR(255))
-- corrections(id INT AUTO_INCREMENT, user_id INT, project_id INT, bonus_points DECIMAL(5, 2))

DELIMITER //

CREATE PROCEDURE AddBonus(
    IN p_user_id INT, 
    IN p_project_name VARCHAR(255), 
    IN p_bonus_points DECIMAL(5, 2)
)
BEGIN
    DECLARE v_project_id INT;

    -- Check if the project name already exists
    SELECT id INTO v_project_id 
    FROM projects 
    WHERE name = p_project_name
    LIMIT 1;

    -- If no project found, insert it
    IF v_project_id IS NULL THEN
        INSERT INTO projects (name) 
        VALUES (p_project_name);
        
        -- Get the last inserted project id
        SET v_project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the correction entry with the user_id, project_id, and bonus_points
    INSERT INTO corrections (user_id, project_id, bonus_points)
    VALUES (p_user_id, v_project_id, p_bonus_points);
    
END //

DELIMITER ;
