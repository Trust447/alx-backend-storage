SELECT u.id, u.name, 
       IFNULL(AVG(c.score), 0) AS average_score
FROM users u
LEFT JOIN corrections c ON u.id = c.user_id
GROUP BY u.id;
