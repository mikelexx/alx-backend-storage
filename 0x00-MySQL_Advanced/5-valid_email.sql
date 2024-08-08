-- Write a SQL script that creates a trigger that resets the attribute valid_email only when the email has been changed.
--
-- Context: Nothing related to MySQL, but perfect for user email validation - distribute the logic to the database itself!

DROP TRIGGER IF EXISTS reset_valid_email;

CREATE
DEFINER = CURRENT_USER
TRIGGER reset_valid_email
BEFORE UPDATE
ON users FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = OLD.valid_email;
    END IF;
END;
DROP TRIGGER IF EXISTS update_quantity; 
