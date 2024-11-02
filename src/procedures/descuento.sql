CREATE OR REPLACE PROCEDURE sp_register_descuento(
  i_codigo          VARCHAR,
  i_monto           DECIMAL(8, 2),
  i_estado          VARCHAR,
  i_id_admin        INT,
  OUT last_id       INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  INSERT INTO descuento (codigo, monto, estado, id_admin)
  VALUES (i_codigo, i_monto, i_estado, i_id_admin)
  RETURNING id_descuento INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El descuento ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el descuento';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_descuento_by_id(i_id_descuento INT)
RETURNS TABLE(
  id_descuento    INT,
  codigo          VARCHAR,
  monto           DECIMAL(8, 2),
  estado          VARCHAR,
  id_admin        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT d.id_descuento, d.codigo, d.monto, d.estado, d.id_admin
  FROM descuento d
  WHERE d.id_descuento = i_id_descuento;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_descuento_all()
RETURNS TABLE(
  id_descuento    INT,
  codigo          VARCHAR,
  monto           DECIMAL(8, 2),
  estado          VARCHAR,
  id_admin        INT
) AS $$
BEGIN
  SELECT d.id_descuento, d.codigo, d.monto, d.estado, d.id_admin
  FROM descuento d;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_descuento_by_id(
  i_id_descuento   INT,
  i_codigo         VARCHAR,
  i_monto          DECIMAL(8, 2),
  i_estado         VARCHAR,
  i_id_admin       INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE descuento
  SET codigo = i_codigo,
      monto = i_monto,
      estado = i_estado,
      id_admin = i_id_admin
  WHERE id_descuento = i_id_descuento;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del descuento ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en descuento table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;
