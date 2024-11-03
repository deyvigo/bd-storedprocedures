CREATE PROCEDURE IF NOT EXISTS sp_register_viaje_programado(
  IN  i_fecha_salida        timestamp,
  IN  i_hora_salida         time,
  IN  i_precio_nivel_uno    decimal(8, 2),
  IN  i_precio_nivel_dos    decimal(8, 2),
  IN  i_asientos_ocupados   int,
  IN  i_id_ruta             int,
  IN  i_id_bus              int,
  IN  i_id_admin_created    int,
  IN  i_id_chofer           int,
  OUT last_id               int,
  OUT rows_affected         int,
  OUT error_message         varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el viaje de programado';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO viaje_programado (fecha_salida, hora_salida, precio_nivel_uno, precio_nivel_dos, asientos_ocupados, id_ruta, id_bus, id_admin_created, id_chofer)
  VALUES (i_fecha_salida, i_hora_salida, i_precio_nivel_uno, i_precio_nivel_dos, i_asientos_ocupados, i_id_ruta, i_id_bus, i_id_admin_created, i_id_chofer);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_viaje_programado_by_id(
  IN  i_id_viaje_programado int
)
BEGIN
  SELECT * FROM viaje_programado WHERE id_viaje_programado = i_id_viaje_programado;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_viaje_programado_all()
BEGIN
  SELECT * FROM viaje_programado;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_viaje_programado_by_id(
  IN  i_id_viaje_programado int,
  IN  i_fecha_salida        timestamp,
  IN  i_hora_salida         time,
  IN  i_precio_nivel_uno    decimal(8, 2),
  IN  i_precio_nivel_dos    decimal(8, 2),
  IN  i_asientos_ocupados   int,
  IN  i_id_ruta             int,
  IN  i_id_bus              int,
  IN  i_id_admin_created    int,
  IN  i_id_chofer           int,
  OUT rows_affected         int,
  OUT error_message         varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el viaje de programado';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE viaje_programado
  SET fecha_salida = i_fecha_salida, hora_salida = i_hora_salida, precio_nivel_uno = i_precio_nivel_uno, precio_nivel_dos = i_precio_nivel_dos, asientos_ocupados = i_asientos_ocupados, id_ruta = i_id_ruta, id_bus = i_id_bus, id_admin_created = i_id_admin_created, id_chofer = i_id_chofer
  WHERE id_viaje_programado = i_id_viaje_programado;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;