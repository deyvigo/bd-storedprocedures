CREATE OR REPLACE PROCEDURE sp_register_transaccion(
  i_precio_neto       DECIMAL(8, 2),
  i_igv               DECIMAL(8, 2),
  i_precio_total      DECIMAL(8, 2),
  i_fecha_compra      TIMESTAMP,
  i_ruc               VARCHAR,
  i_correo_contacto   VARCHAR,
  i_telefono_contacto VARCHAR,
  i_id_cliente        INT,
  i_id_descuento      INT,
  i_id_tipo_boleta    INT,
  i_id_metodo_pago    INT,
  OUT last_id         INT,
  OUT rows_affected   INT,
  OUT error_message   VARCHAR
) AS $$
BEGIN
  INSERT INTO transaccion (precio_neto, igv, precio_total, fecha_compra, ruc, correo_contacto, telefono_contacto, id_cliente, id_descuento, id_tipo_boleta, id_metodo_pago)
  VALUES (i_precio_neto, i_igv, i_precio_total, i_fecha_compra, i_ruc, i_correo_contacto, i_telefono_contacto, i_id_cliente, i_id_descuento, i_id_tipo_boleta, i_id_metodo_pago)
  RETURNING id_transaccion INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El transaccion ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar la transaccion';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_transaccion_by_id(i_id_transaccion INT)
RETURNS TABLE(
  id_transaccion    INT,
  precio_neto       DECIMAL(8, 2),
  igv               DECIMAL(8, 2),
  precio_total      DECIMAL(8, 2),
  fecha_compra      TIMESTAMP,
  ruc               VARCHAR,
  correo_contacto   VARCHAR,
  telefono_contacto VARCHAR,
  id_cliente        INT,
  id_descuento      INT,
  id_tipo_boleta    INT,
  id_metodo_pago    INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_transaccion, t.precio_neto, t.igv, t.precio_total, t.fecha_compra, t.ruc, t.correo_contacto, t.telefono_contacto, t.id_cliente, t.id_descuento, t.id_tipo_boleta, t.id_metodo_pago
  FROM transaccion t
  WHERE t.id_transaccion = i_id_transaccion;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_transaccion_all()
RETURNS TABLE(
  id_transaccion    INT,
  precio_neto       DECIMAL(8, 2),
  igv               DECIMAL(8, 2),
  precio_total      DECIMAL(8, 2),
  fecha_compra      TIMESTAMP,
  ruc               VARCHAR,
  correo_contacto   VARCHAR,
  telefono_contacto VARCHAR,
  id_cliente        INT,
  id_descuento      INT,
  id_tipo_boleta    INT,
  id_metodo_pago    INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_transaccion, t.precio_neto, t.igv, t.precio_total, t.fecha_compra, t.ruc, t.correo_contacto, t.telefono_contacto, t.id_cliente, t.id_descuento, t.id_tipo_boleta, t.id_metodo_pago
  FROM transaccion t;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_transaccion_by_id(
  i_id_transaccion    INT,
  i_precio_neto       DECIMAL(8, 2),
  i_igv               DECIMAL(8, 2),
  i_precio_total      DECIMAL(8, 2),
  i_fecha_compra      TIMESTAMP,
  i_ruc               VARCHAR,
  i_correo_contacto   VARCHAR,
  i_telefono_contacto VARCHAR,
  i_id_cliente        INT,
  i_id_descuento      INT,
  i_id_tipo_boleta    INT,
  i_id_metodo_pago    INT,
  OUT rows_affected   INT,
  OUT error_message   VARCHAR
) AS $$
BEGIN
  UPDATE transaccion
  SET precio_neto = i_precio_neto,
      igv = i_igv,
      precio_total = i_precio_total,
      fecha_compra = i_fecha_compra,
      ruc = i_ruc,
      correo_contacto = i_correo_contacto,
      telefono_contacto = i_telefono_contacto,
      id_cliente = i_id_cliente,
      id_descuento = i_id_descuento,
      id_tipo_boleta = i_id_tipo_boleta,
      id_metodo_pago = i_id_metodo_pago
  WHERE id_transaccion = i_id_transaccion;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos de la transaccion ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en transaccion table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_get_transaccion_by_id_cliente(
  i_id_cliente INT
)
RETURNS TABLE(
  id_transaccion    INT,
  fecha_compra      TIMESTAMP,
  precio_total      DECIMAL(8, 2),
  cantidad_pasajes  INT
)
AS $$
BEGIN
  RETURN QUERY
  SELECT
    tr.id_transaccion,
    tr.fecha_compra::TIMESTAMP AS fecha_compra,
    tr.precio_total,
    COUNT(p.id_transaccion)::INT AS cantidad_pasajes
  FROM transaccion tr
  JOIN pasaje p ON p.id_transaccion = tr.id_transaccion
  WHERE tr.id_cliente = i_id_cliente
  GROUP BY tr.id_transaccion
  ORDER BY tr.fecha_compra ASC;
END;
$$ LANGUAGE plpgsql;