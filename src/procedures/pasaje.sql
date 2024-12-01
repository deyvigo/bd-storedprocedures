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

CREATE OR REPLACE FUNCTION fn_get_pasaje_by_id_cliente(
  i_id_cliente INT
)
RETURNS TABLE(
  id_pasaje           INT,
  precio_total        DECIMAL(8, 2),
  fecha_salida        TIMESTAMP,
  puerto_salida       VARCHAR,
  puerto_destino      VARCHAR,
  nombre_pasajero     VARCHAR,
  hora_salida         TIME,
  fecha_compra        TIMESTAMP
)
AS $$
BEGIN
  RETURN QUERY
  SELECT
    p.id_pasaje,
    p.precio_total as precio,
    vp.fecha_salida::TIMESTAMP as fecha_salida,
    te_origen.nombre as puerto_salida,
    te_destino.nombre as puerto_destino,
    CONCAT(pa.nombre, ', ', pa.apellido_pat, ' ', pa.apellido_mat)::VARCHAR as nombre_pasajero,
    vp.hora_salida,
    t.fecha_compra
  FROM pasaje p
  JOIN viaje_programado vp ON vp.id_viaje_programado = p.id_viaje_programado
  JOIN ruta r ON r.id_ruta = vp.id_ruta
  JOIN terminal te_origen ON te_origen.id_terminal = r.id_origen
  JOIN terminal te_destino ON te_destino.id_terminal = r.id_destino
  JOIN pasajero pa ON pa.id_pasajero = p.id_pasajero
  JOIN transaccion t ON t.id_transaccion = p.id_transaccion
  JOIN cliente c ON c.id_cliente =  t.id_cliente
  WHERE c.id_cliente = i_id_cliente
  ORDER BY t.fecha_compra ASC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_get_pasaje_by_id_pasaje_for_pdf(
  i_id_pasaje INT
)
RETURNS TABLE(
  id_transaccion   INT,
  id_pasaje        INT,
  embarque         VARCHAR,
  desembarque      VARCHAR,
  fecha_salida     TIMESTAMP,
  hora_salida      TIME,
  asiento          INT,
  piso             INT,
  servicio         VARCHAR,
  pasajero         VARCHAR,
  dni              VARCHAR,
  precio_neto      DECIMAL(8, 2),
  igv              DECIMAL(8, 2),
  precio_total     DECIMAL(8, 2),
  numero_tarjeta   VARCHAR
)
AS $$
BEGIN
  RETURN QUERY
  SELECT
    t.id_transaccion,
    p.id_pasaje,
    CONCAT(te_origen.nombre, ' - ', te_origen.departamento)::VARCHAR as embarque,
    CONCAT(te_destino.nombre, ' - ', te_destino.departamento)::VARCHAR as desembarque,
    vp.fecha_salida::TIMESTAMP as fecha_salida,
    vp.hora_salida,
    a.numero as asiento,
    a.nivel as piso,
    tsb.servicio,
    CONCAT(pa.nombre, ', ', pa.apellido_pat, ' ', pa.apellido_mat)::VARCHAR as pasajero,
    pa.dni,
    p.precio_neto,
    p.igv,
    p.precio_total,
    mp.numero_tarjeta
  FROM pasaje p
  JOIN viaje_programado vp ON vp.id_viaje_programado = p.id_viaje_programado
  JOIN asiento a ON a.id_asiento = p.id_asiento
  JOIN bus b ON b.id_bus = vp.id_bus
  JOIN tipo_servicio_bus tsb ON tsb.id_tipo_servicio_bus = b.id_tipo_servicio_bus
  JOIN ruta r ON r.id_ruta = vp.id_ruta
  JOIN terminal te_origen ON te_origen.id_terminal = r.id_origen
  JOIN terminal te_destino ON te_destino.id_terminal = r.id_destino
  JOIN pasajero pa ON pa.id_pasajero = p.id_pasajero
  JOIN transaccion t ON t.id_transaccion = p.id_transaccion
  JOIN metodo_pago mp ON mp.id_metodo_pago = t.id_metodo_pago
  WHERE p.id_pasaje = i_id_pasaje;
END;
$$ LANGUAGE plpgsql;