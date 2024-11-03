CREATE OR REPLACE PROCEDURE sp_register_pasaje(
  i_fecha_compra        TIMESTAMP,
  i_precio_neto         DECIMAL(8, 2),
  i_igv                 DECIMAL(8, 2),
  i_precio_total        DECIMAL(8, 2),
  i_id_pasajero         INT,
  i_id_asiento          INT,
  i_id_viaje_programado INT,
  i_id_transaccion      INT,
  i_fecha_modificacion  TIMESTAMP,
  i_id_admin_mod        INT,
  OUT last_id           INT,
  OUT rows_affected     INT,
  OUT error_message     VARCHAR
) AS $$
BEGIN
  INSERT INTO pasaje (fecha_compra, precio_neto, igv, precio_total, id_pasajero, id_asiento, id_viaje_programado, id_transaccion, fecha_modificacion, id_admin_mod)
  VALUES (i_fecha_compra, i_precio_neto, i_igv, i_precio_total, i_id_pasajero, i_id_asiento, i_id_viaje_programado, i_id_transaccion, i_fecha_modificacion, i_id_admin_mod)
  RETURNING id_pasaje INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El pasaje ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el pasaje';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_pasaje_by_id(i_id_pasaje INT)
RETURNS TABLE(
  id_pasaje           INT,
  fecha_compra        TIMESTAMP,
  precio_neto         DECIMAL(8, 2),
  igv                 DECIMAL(8, 2),
  precio_total        DECIMAL(8, 2),
  id_pasajero         INT,
  id_asiento          INT,
  id_viaje_programado INT,
  id_transaccion      INT,
  fecha_modificacion  TIMESTAMP,
  id_admin_mod        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id_pasaje, p.fecha_compra, p.precio_neto, p.igv, p.precio_total, p.id_pasajero, p.id_asiento, p.id_viaje_programado, p.id_transaccion, p.fecha_modificacion, p.id_admin_mod
  FROM pasaje p
  WHERE p.id_pasaje = i_id_pasaje;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_pasaje_all()
RETURNS TABLE(
  id_pasaje           INT,
  fecha_compra        TIMESTAMP,
  precio_neto         DECIMAL(8, 2),
  igv                 DECIMAL(8, 2),
  precio_total        DECIMAL(8, 2),
  id_pasajero         INT,
  id_asiento          INT,
  id_viaje_programado INT,
  id_transaccion      INT,
  fecha_modificacion  TIMESTAMP,
  id_admin_mod        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id_pasaje, p.fecha_compra, p.precio_neto, p.igv, p.precio_total, p.id_pasajero, p.id_asiento, p.id_viaje_programado, p.id_transaccion, p.fecha_modificacion, p.id_admin_mod
  FROM pasaje p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_pasaje_by_id(
  i_id_pasaje           INT,
  i_fecha_compra        TIMESTAMP,
  i_precio_neto         DECIMAL(8, 2),
  i_igv                 DECIMAL(8, 2),
  i_precio_total        DECIMAL(8, 2),
  i_id_pasajero         INT,
  i_id_asiento          INT,
  i_id_viaje_programado INT,
  i_id_transaccion      INT,
  i_fecha_modificacion  TIMESTAMP,
  i_id_admin_mod        INT,
  OUT rows_affected     INT,
  OUT error_message     VARCHAR
) AS $$
BEGIN
  UPDATE pasaje
  SET fecha_compra = i_fecha_compra,
      precio_neto = i_precio_neto,
      igv = i_igv,
      precio_total = i_precio_total,
      id_pasajero = i_id_pasajero,
      id_asiento = i_id_asiento,
      id_viaje_programado = i_id_viaje_programado,
      id_transaccion = i_id_transaccion,
      fecha_modificacion = i_fecha_modificacion,
      id_admin_mod = i_id_admin_mod
  WHERE id_pasaje = i_id_pasaje;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del pasaje ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en pasaje table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;