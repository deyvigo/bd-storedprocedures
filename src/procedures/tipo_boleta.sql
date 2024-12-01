CREATE PROCEDURE IF NOT EXISTS sp_register_tipo_boleta(
  IN  i_tipo           varchar(20),
  OUT last_id          int,
  OUT rows_affected    int,
  OUT error_message    varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el tipo de boleta';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO tipo_boleta (tipo) VALUES (i_tipo);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_tipo_boleta_by_id(
  IN  i_id_tipo_boleta int
)
BEGIN
  SELECT * FROM tipo_boleta WHERE id_tipo_boleta = i_id_tipo_boleta;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_tipo_boleta_all()
BEGIN
  SELECT * FROM tipo_boleta;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_tipo_boleta_by_id(
  IN  i_id_tipo_boleta int,
  IN  i_tipo           varchar(20),
  OUT rows_affected    int,
  OUT error_message    varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el tipo de boleta';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE tipo_boleta SET tipo = i_tipo WHERE id_tipo_boleta = i_id_tipo_boleta;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_tipo_boleta_by_tipo(
  IN  i_tipo varchar(20)
)
BEGIN
  SELECT id_tipo_boleta FROM tipo_boleta WHERE tipo = i_tipo;
END;
