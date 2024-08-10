-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.
-- 
-- Requirements:
-- 
-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.
-- Tips:
-- 
-- Calculate-Weighted-Average
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE 
DEFINER = CURRENT_USER
PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE average_score FLOAT;
	DECLARE done INT;
	DECLARE avg_score_user_id INT;
	DECLARE score_cursor CURSOR FOR SELECT corrections.user_id, SUM(corrections.score * weight) / SUM(weight) FROM corrections
	INNER JOIN projects
	ON corrections.project_id = projects.id
	GROUP BY corrections.user_id;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN score_cursor;
	read_avg_scores: LOOP
		FETCH score_cursor INTO avg_score_user_id, average_score;
			UPDATE users
			SET users.average_score = average_score
			WHERE users.id = avg_score_user_id;
		IF done THEN
			LEAVE read_avg_scores;
		END IF;
	END LOOP;
	CLOSE score_cursor;
	END; $$
	DELIMITER ;
