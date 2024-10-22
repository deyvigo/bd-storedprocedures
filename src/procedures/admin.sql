-- Stored Procedure to get an admin by username
CREATE PROCEDURE IF NOT EXISTS get_admin_by_username(
  IN i_username VARCHAR(50)
)
BEGIN
  SELECT * FROM admin WHERE username = i_username;
END;