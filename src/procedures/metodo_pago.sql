CREATE OR REPLACE PROCEDURE sp_register_metodo_pago(
  i_nombre            VARCHAR,
  i_numero_tarjeta    VARCHAR,
  i_id_cliente        INT,
  OUT last_id         INT,
  OUT rows_affected   INT,
  OUT error_message   VARCHAR
) AS $$
BEGIN
  INSERT INTO metodo_pago (nombre, numero_tarjeta, id_cliente)
  VALUES (i_nombre, i_numero_tarjeta, i_id_cliente)
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
  nombre            VARCHAR,
  numero_tarjeta    VARCHAR,
  estado            VARCHAR,
  id_cliente        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT m.id_metodo_pago, m.nombre, m.estado, m.numero_tarjeta, m.id_cliente
  FROM metodo_pago m
  WHERE m.id_metodo_pago = i_id_metodo_pago;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_metodo_pago_all()
RETURNS TABLE(
  id_metodo_pago    INT,
  nombre            VARCHAR,
  numero_tarjeta    VARCHAR,
  id_cliente        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT m.id_metodo_pago, m.nombre, m.estado, m.numero_tarjeta, m.id_cliente
  FROM metodo_pago m;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_metodo_pago_by_id(
  i_id_metodo_pago  INT,
  i_metodo          VARCHAR,
  i_numero_tarjeta  VARCHAR,
  i_id_cliente      INT,
  i_estado          VARCHAR,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE metodo_pago
  SET metodo = i_metodo,
      numero_tarjeta = i_numero_tarjeta,
      id_cliente = i_id_cliente,
      estado = i_estado
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