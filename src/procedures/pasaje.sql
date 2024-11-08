CREATE PROCEDURE IF NOT EXISTS sp_register_pasaje(
  IN  i_fecha_compra        timestamp,
  IN  i_precio_neto         decimal(8, 2),
  IN  i_igv                 decimal(8, 2),
  IN  i_precio_total        decimal(8, 2),
  IN  i_id_pasajero         int,
  IN  i_id_asiento          int,
  IN  i_id_viaje_programado int,
  IN  i_id_transaccion      int,
  IN  i_fecha_modificacion  timestamp,
  IN  i_id_admin_mod        int,
  OUT last_id               int,
  OUT rows_affected         int,
  OUT error_message         varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el pasaje';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO pasaje (fecha_compra, precio_neto, igv, precio_total, id_pasajero, id_asiento, id_viaje_programado, id_transaccion, fecha_modificacion, id_admin_mod)
  VALUES (i_fecha_compra, i_precio_neto, i_igv, i_precio_total, i_id_pasajero, i_id_asiento, i_id_viaje_programado, i_id_transaccion, i_fecha_modificacion, i_id_admin_mod);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_pasaje_by_id(
  IN  i_id_pasaje int
)
BEGIN
  SELECT * FROM pasaje WHERE id_pasaje = i_id_pasaje;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_pasaje_all()
BEGIN
  SELECT * FROM pasaje;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_pasaje_by_id(
  IN  i_id_pasaje           int,
  IN  i_fecha_compra        timestamp,
  IN  i_precio_neto         decimal(8, 2),
  IN  i_igv                 decimal(8, 2),
  IN  i_precio_total        decimal(8, 2),
  IN  i_id_pasajero         int,
  IN  i_id_asiento          int,
  IN  i_id_viaje_programado int,
  IN  i_id_transaccion      int,
  IN  i_fecha_modificacion  timestamp,
  IN  i_id_admin_mod        int,
  OUT rows_affected         int,
  OUT error_message         varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el pasaje';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE pasaje
  SET fecha_compra = i_fecha_compra, precio_neto = i_precio_neto, igv = i_igv, precio_total = i_precio_total, id_pasajero = i_id_pasajero, id_asiento = i_id_asiento, id_viaje_programado = i_id_viaje_programado, id_transaccion = i_id_transaccion, fecha_modificacion = i_fecha_modificacion, id_admin_mod = i_id_admin_mod
  WHERE id_pasaje = i_id_pasaje;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;