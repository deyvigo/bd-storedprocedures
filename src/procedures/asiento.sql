CREATE PROCEDURE IF NOT EXISTS sp_register_asiento(
  IN  i_nivel            int,
  IN  i_numero           int,
  IN  i_id_bus           int,
  OUT last_id            int,
  OUT rows_affected      int,
  OUT error_message      varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el asiento';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO asiento (nivel, numero, id_bus) VALUES (i_nivel, i_numero, i_id_bus);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_asiento_by_id(
  IN  i_id_asiento int
)
BEGIN
  SELECT * FROM asiento WHERE id_asiento = i_id_asiento;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_asiento_all()
BEGIN
  SELECT * FROM asiento;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_asiento_by_id(
  IN  i_id_asiento      int,
  IN  i_nivel           int,
  IN  i_numero          int,
  IN  i_id_bus          int,
  OUT rows_affected     int,
  OUT error_message     varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el asiento';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE asiento SET nivel = i_nivel, numero = i_numero, id_bus = i_id_bus WHERE id_asiento = i_id_asiento;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;