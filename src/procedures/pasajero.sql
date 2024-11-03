CREATE PROCEDURE IF NOT EXISTS sp_register_pasajero(
  IN  i_dni              varchar(8),
  IN  i_nombre           varchar(255),
  IN  i_apellido_pat     varchar(50),
  IN  i_apellido_mat     varchar(50),
  IN  i_fecha_nacimiento date,
  IN  i_sexo             varchar(15),
  OUT last_id            int,
  OUT rows_affected      int,
  OUT error_message      varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el pasajero';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO pasajero (dni, nombre, apellido_pat, apellido_mat, fecha_nacimiento, sexo)
  VALUES (i_dni, i_nombre, i_apellido_pat, i_apellido_mat, i_fecha_nacimiento, i_sexo);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_pasajero_by_id(
  IN  i_id_pasajero int
)
BEGIN
  SELECT * FROM pasajero WHERE id_pasajero = i_id_pasajero;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_pasajero_all()
BEGIN
  SELECT * FROM pasajero;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_pasajero_by_id(
  IN  i_id_pasajero    int,
  IN  i_dni            varchar(8),
  IN  i_nombre         varchar(255),
  IN  i_apellido_pat   varchar(50),
  IN  i_apellido_mat   varchar(50),
  IN  i_fecha_nacimiento date,
  IN  i_sexo           varchar(15),
  OUT rows_affected    int,
  OUT error_message    varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el pasajero';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE pasajero
  SET dni = i_dni, nombre = i_nombre, apellido_pat = i_apellido_pat, apellido_mat = i_apellido_mat, fecha_nacimiento = i_fecha_nacimiento, sexo = i_sexo
  WHERE id_pasajero = i_id_pasajero;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;