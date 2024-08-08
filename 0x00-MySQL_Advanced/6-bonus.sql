-- Write a SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
-- 
-- Requirements:
-- 
-- Procedure AddBonus is taking 3 inputs (in this order):
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
-- project_name, a new or already exists projects - if no projects.name found in the table, you should create it
-- score, the score value for the correction
-- Context: Write code in SQL is a nice level up!
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE
DEFINER = CURRENT_USER
PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
	DECLARE project_id INT;
	IF project_name NOT IN (SELECT name FROM projects WHERE name =  project_name) THEN
		INSERT INTO projects
		(name)
		VALUES (project_name);
	END IF;
	SELECT id INTO project_id 
	FROM projects
	WHERE name = project_name;
	INSERT
	INTO corrections
	(user_id, project_id, score)
	VALUES (user_id, project_id, score);
END; $$
DELIMITER ;
