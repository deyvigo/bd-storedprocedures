CREATE PROCEDURE IF NOT EXISTS sp_get_admin_by_username(
  IN i_username varchar(50)
)
BEGIN
  SELECT * FROM admin WHERE username = i_username;
END;

CREATE PROCEDURE IF NOT EXISTS sp_register_admin(
  IN  i_nombre           varchar(255),
  IN  i_apellido_pat     varchar(50),
  IN  i_apellido_mat     varchar(50),
  IN  i_fecha_nacimiento date,
  IN  i_dni              varchar(8),
  IN  i_sexo             varchar(15),
  IN  i_telefono         varchar(20),
  IN  i_correo           varchar(255),
  IN  i_username         varchar(50),
  IN  i_password         varchar(80),
  OUT rows_affected      int,
  OUT last_id            int,
  OUT error_message      varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el administrador';
    SET last_id = -1;
    ROLLBACK;
  END;

  START TRANSACTION;
  IF EXISTS (SELECT 1 FROM admin WHERE username = i_username) THEN
    SET rows_affected = 0;
    SET error_message = 'El username del administrador ya existe';
    SET last_id = 0;
    ROLLBACK;
  ELSE
    INSERT INTO admin (
      nombre, apellido_pat, apellido_mat, fecha_nacimiento, dni, sexo, telefono, correo, username, password
    )
    VALUES (
      i_nombre, i_apellido_pat, i_apellido_mat, i_fecha_nacimiento, i_dni, i_sexo, i_telefono, i_correo, i_username, i_password
    );
    SET rows_affected = ROW_COUNT();
    SET last_id = LAST_INSERT_ID();
    SET error_message = NULL;
    COMMIT;
  END IF;
END;