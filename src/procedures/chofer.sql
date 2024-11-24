CREATE PROCEDURE IF NOT EXISTS sp_register_chofer(
  IN  i_nombre          varchar(255),
  IN  i_apellido_pat    varchar(50),
  IN  i_apellido_mat    varchar(50),
  IN  i_dni             varchar(8),
  IN  i_sexo            varchar(15),
  OUT last_id           int,
  OUT rows_affected     int,
  OUT error_message     varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el chofer';
    SET last_id = -1;
    ROLLBACK;
  END;

  START TRANSACTION;

  IF EXISTS (SELECT 1 FROM chofer WHERE dni = i_dni) THEN
    SET rows_affected = 0;
    SET error_message = 'El DNI del chofer ya existe';
    SET last_id = 0;
    ROLLBACK;
  ELSE
    CALL sp_add_chofer(i_nombre, i_apellido_pat, i_apellido_mat, i_dni, i_sexo, 'contratado');
    SET rows_affected = ROW_COUNT();
    SET last_id = LAST_INSERT_ID();
    SET error_message = NULL;
    COMMIT;
  END IF;  
END;

CREATE PROCEDURE IF NOT EXISTS sp_add_chofer(
  IN  i_nombre         varchar(255),
  IN  i_apellido_pat   varchar(50),
  IN  i_apellido_mat   varchar(50),
  IN  i_dni            varchar(8),
  IN  i_sexo           varchar(15),
  IN  i_estado        varchar(15)
)
BEGIN
  INSERT INTO chofer(nombre, apellido_pat, apellido_mat, dni, sexo, estado)
  VALUES (i_nombre, i_apellido_pat, i_apellido_mat, i_dni, i_sexo, i_estado);
END;


CREATE PROCEDURE IF NOT EXISTS sp_get_chofer_by_id(
  IN  i_id_chofer int
)
BEGIN
  SELECT * FROM chofer WHERE id_chofer = i_id_chofer;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_chofer_all()
BEGIN
  SELECT * FROM chofer;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_hired_chofer()
BEGIN
  SELECT * FROM chofer WHERE estado = 'contratado';
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_fired_chofer()
BEGIN
  SELECT * FROM chofer WHERE estado = 'despedido';
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_chofer_by_id(
  IN  i_id_chofer      int,
  IN  i_nombre         varchar(255),
  IN  i_apellido_pat   varchar(50),
  IN  i_apellido_mat   varchar(50),
  IN  i_dni            varchar(8),
  IN  i_sexo           varchar(15),
  OUT rows_affected    int,
  OUT error_message    varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el chofer';
    ROLLBACK;
  END;

  START TRANSACTION;
  UPDATE chofer
  SET nombre = i_nombre, apellido_pat = i_apellido_pat, apellido_mat = i_apellido_mat, sexo = i_sexo, dni = i_dni
  WHERE id_chofer = i_id_chofer;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_status_chofer_by_id(
  IN  i_id_chofer      int,
  OUT rows_affected    int,
  OUT error_message    varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el chofer';
    ROLLBACK;
  END;

  START TRANSACTION;
  UPDATE chofer
  SET estado = CASE
                 WHEN estado = 'contratado' THEN 'despedido'
                 WHEN estado = 'despedido' THEN 'contratado'
               END
  WHERE id_chofer = i_id_chofer;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_free_chofer(
  IN  i_date date
)
BEGIN
  SELECT chofer.id_chofer 
  FROM chofer
  LEFT JOIN viajes_programados 
    ON chofer.id_chofer = viajes_programados.id_chofer 
    AND viajes_programados.fecha_viaje BETWEEN i_date AND DATE_ADD(i_date, INTERVAL 1 DAY)
  WHERE chofer.estado = 'contratado'
    AND viajes_programados.id_chofer IS NULL;
END;