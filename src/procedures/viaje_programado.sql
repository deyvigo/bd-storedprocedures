CREATE OR REPLACE PROCEDURE sp_register_viaje_programado(
  i_fecha_salida        TIMESTAMP,
  i_hora_salida         TIME,
  i_precio_nivel_uno    DECIMAL(8, 2),
  i_precio_nivel_dos    DECIMAL(8, 2),
  i_asientos_ocupados   INT,
  i_id_ruta             INT,
  i_id_bus              INT,
  i_id_admin_created    INT,
  i_id_chofer           INT,
  OUT last_id           INT,
  OUT rows_affected     INT,
  OUT error_message     VARCHAR
) AS $$
BEGIN
  INSERT INTO viaje_programado (fecha_salida, hora_salida, precio_nivel_uno, precio_nivel_dos, asientos_ocupados, id_ruta, id_bus, id_admin_created, id_chofer)
  VALUES (i_fecha_salida, i_hora_salida, i_precio_nivel_uno, i_precio_nivel_dos, i_asientos_ocupados, i_id_ruta, i_id_bus, i_id_admin_created, i_id_chofer)
  RETURNING id_viaje_programado INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El viaje de programado ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el viaje de programado';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_viaje_programado_by_id(i_id_viaje_programado INT)
RETURNS TABLE(
  id_viaje_programado INT,
  fecha_salida        TIMESTAMP,
  hora_salida         TIME,
  precio_nivel_uno    DECIMAL(8, 2),
  precio_nivel_dos    DECIMAL(8, 2),
  asientos_ocupados   INT,
  id_ruta             INT,
  id_bus              INT,
  id_admin_created    INT,
  id_chofer           INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT v.id_viaje_programado, v.fecha_salida, v.hora_salida, v.precio_nivel_uno, v.precio_nivel_dos, v.asientos_ocupados, v.id_ruta, v.id_bus, v.id_admin_created, v.id_chofer
  FROM viaje_programado v
  WHERE v.id_viaje_programado = i_id_viaje_programado;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_viaje_programado_all()
RETURNS TABLE(
  id_viaje_programado INT,
  fecha_salida        TIMESTAMP,
  hora_salida         TIME,
  precio_nivel_uno    DECIMAL(8, 2),
  precio_nivel_dos    DECIMAL(8, 2),
  asientos_ocupados   INT,
  id_ruta             INT,
  id_bus              INT,
  id_admin_created    INT,
  id_chofer           INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT v.id_viaje_programado, v.fecha_salida, v.hora_salida, v.precio_nivel_uno, v.precio_nivel_dos, v.asientos_ocupados, v.id_ruta, v.id_bus, v.id_admin_created, v.id_chofer
  FROM viaje_programado v;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_viaje_programado_by_id(
  i_id_viaje_programado INT,
  i_fecha_salida        TIMESTAMP,
  i_hora_salida         TIME,
  i_precio_nivel_uno    DECIMAL(8, 2),
  i_precio_nivel_dos    DECIMAL(8, 2),
  i_asientos_ocupados   INT,
  i_id_ruta             INT,
  i_id_bus              INT,
  i_id_admin_created    INT,
  i_id_chofer           INT,
  OUT rows_affected     INT,
  OUT error_message     VARCHAR
) AS $$
BEGIN
  UPDATE viaje_programado
  SET fecha_salida = i_fecha_salida,
      hora_salida = i_hora_salida,
      precio_nivel_uno = i_precio_nivel_uno,
      precio_nivel_dos = i_precio_nivel_dos,
      asientos_ocupados = i_asientos_ocupados,
      id_ruta = i_id_ruta,
      id_bus = i_id_bus,
      id_admin_created = i_id_admin_created,
      id_chofer = i_id_chofer
  WHERE id_viaje_programado = i_id_viaje_programado;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del viaje de programado ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en viaje de programado table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;