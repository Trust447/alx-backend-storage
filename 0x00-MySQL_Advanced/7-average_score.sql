DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(5, 2); -- Adjust precision and scale as needed

    -- Calculate the average score for the user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = p_user_id;

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = IFNULL(avg_score, 0) -- Set to 0 if no scores found
    WHERE id = p_user_id;

END $$

DELIMITER ;

