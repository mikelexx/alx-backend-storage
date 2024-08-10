-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
-- 
-- Requirements:
-- 
-- Procedure ComputeAverageScoreForUser is taking 1 input:
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- Tips:
-- 
-- Calculate-Weighted-Average
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE 
DEFINER = CURRENT_USER
PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
	DECLARE average_score INT;
	DECLARE done INT;
	DECLARE score_cursor CURSOR FOR SELECT corrections.user_id, SUM(corrections.score * weight) / SUM(weight) FROM corrections
	LEFT JOIN projects
	ON corrections.project_id = projects.id
	GROUP BY corrections.user_id;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN score_cursor;
	read_avg_scores: LOOP
		FETCH score_cursor INTO user_id, average_score;
		UPDATE users
		SET users.average_score = average_score
		WHERE users.id = user_id;
		IF done THEN
			LEAVE read_avg_scores;
		END IF;
	END LOOP;
	END; $$
	DELIMITER ;
