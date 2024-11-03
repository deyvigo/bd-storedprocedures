CREATE PROCEDURE IF NOT EXISTS sp_register_ruta(
  IN  i_duracion_estimada time,
  IN  i_distancia         double precision,
  IN  i_estado            varchar(20),
  IN  i_id_origen         int,
  IN  i_id_destino        int,
  OUT last_id             int,
  OUT rows_affected       int,
  OUT error_message       varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar la ruta';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO ruta (duracion_estimada, distancia, estado, id_origen, id_destino)
  VALUES (i_duracion_estimada, i_distancia, i_estado, i_id_origen, i_id_destino);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_ruta_by_id(
  IN  i_id_ruta int
)
BEGIN
  SELECT * FROM ruta WHERE id_ruta = i_id_ruta;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_ruta_all()
BEGIN
  SELECT * FROM ruta;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_ruta_by_id(
  IN  i_id_ruta           int,
  IN  i_duracion_estimada time,
  IN  i_distancia         double precision,
  IN  i_estado            varchar(20),
  IN  i_id_origen         int,
  IN  i_id_destino        int,
  OUT rows_affected       int,
  OUT error_message       varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar la ruta';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE ruta
  SET duracion_estimada = i_duracion_estimada, distancia = i_distancia, estado = i_estado, id_origen = i_id_origen, id_destino = i_id_destino
  WHERE id_ruta = i_id_ruta;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;