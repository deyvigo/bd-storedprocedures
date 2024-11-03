CREATE PROCEDURE IF NOT EXISTS sp_register_parada_intermedia(
  IN  i_ordinal              int,
  IN  i_id_terminal          int,
  IN  i_id_ruta              int,
  OUT last_id                int,
  OUT rows_affected          int,
  OUT error_message          varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar la parada intermedia';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO parada_intermedia (ordinal, id_terminal, id_ruta)
  VALUES (i_ordinal, i_id_terminal, i_id_ruta);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_parada_intermedia_by_id(
  IN  i_id_parada_intermedia int
)
BEGIN
  SELECT * FROM parada_intermedia WHERE id_parada_intermedia = i_id_parada_intermedia;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_parada_intermedia_all()
BEGIN
  SELECT * FROM parada_intermedia;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_parada_intermedia_by_id(
  IN  i_id_parada_intermedia int,
  IN  i_ordinal              int,
  IN  i_id_terminal          int,
  IN  i_id_ruta              int,
  OUT rows_affected          int,
  OUT error_message          varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar la parada intermedia';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE parada_intermedia
  SET ordinal = i_ordinal, id_terminal = i_id_terminal, id_ruta = i_id_ruta
  WHERE id_parada_intermedia = i_id_parada_intermedia;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;