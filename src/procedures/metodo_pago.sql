CREATE OR REPLACE PROCEDURE sp_register_metodo_pago(
  i_metodo            VARCHAR,
  i_numero_tarjeta    VARCHAR,
  i_cvv               VARCHAR,
  i_fecha_vencimiento VARCHAR,
  i_id_cliente        INT,
  OUT last_id         INT,
  OUT rows_affected   INT,
  OUT error_message   VARCHAR
) AS $$
BEGIN
  INSERT INTO metodo_pago (metodo, numero_tarjeta, cvv, fecha_vencimiento, id_cliente)
  VALUES (i_metodo, i_numero_tarjeta, i_cvv, i_fecha_vencimiento, i_id_cliente)
  RETURNING id_metodo_pago INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El metodo de pago ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el metodo de pago';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_metodo_pago_by_id(i_id_metodo_pago INT)
RETURNS TABLE(
  id_metodo_pago    INT,
  metodo            VARCHAR,
  numero_tarjeta    VARCHAR,
  cvv               VARCHAR,
  fecha_vencimiento VARCHAR,
  id_cliente        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT m.id_metodo_pago, m.metodo, m.numero_tarjeta, m.cvv, m.fecha_vencimiento, m.id_cliente
  FROM metodo_pago m
  WHERE m.id_metodo_pago = i_id_metodo_pago;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_metodo_pago_all()
RETURNS TABLE(
  id_metodo_pago    INT,
  metodo            VARCHAR,
  numero_tarjeta    VARCHAR,
  cvv               VARCHAR,
  fecha_vencimiento VARCHAR,
  id_cliente        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT m.id_metodo_pago, m.metodo, m.numero_tarjeta, m.cvv, m.fecha_vencimiento, m.id_cliente
  FROM metodo_pago m;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_metodo_pago_by_id(
  i_id_metodo_pago  INT,
  i_metodo          VARCHAR,
  i_numero_tarjeta  VARCHAR,
  i_cvv             VARCHAR,
  i_fecha_vencimiento VARCHAR,
  i_id_cliente      INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE metodo_pago
  SET metodo = i_metodo,
      numero_tarjeta = i_numero_tarjeta,
      cvv = i_cvv,
      fecha_vencimiento = i_fecha_vencimiento,
      id_cliente = i_id_cliente
  WHERE id_metodo_pago = i_id_metodo_pago;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del metodo de pago ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en metodo de pago table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;