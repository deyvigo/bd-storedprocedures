CREATE PROCEDURE IF NOT EXISTS check_cliente_username_exists(
  IN  i_username      varchar(50),
  OUT exists_flag     boolean
)
BEGIN
  SELECT COUNT(*) > 0 INTO exists_flag
  FROM cliente
  WHERE username = i_username;
END;

CREATE PROCEDURE IF NOT EXISTS post_cliente(
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
  OUT last_id            int
)
BEGIN
  INSERT INTO cliente (
    nombre, apellido_pat, apellido_mat, fecha_nacimiento, dni, sexo, telefono, correo, username, password
  )
  VALUES (
    i_nombre, i_apellido_pat, i_apellido_mat, i_fecha_nacimiento, i_dni, i_sexo, i_telefono, i_correo, i_username, i_password
  );
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
END;