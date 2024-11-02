CREATE OR REPLACE PROCEDURE sp_register_tipo_boleta(
  i_tipo           VARCHAR,
  OUT last_id      INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  INSERT INTO tipo_boleta (tipo)
  VALUES (i_tipo)
  RETURNING id_tipo_boleta INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El tipo de boleta ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el tipo de boleta';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tipo_boleta_by_id(i_id_tipo_boleta INT)
RETURNS TABLE(
  id_tipo_boleta INT,
  tipo           VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_tipo_boleta, t.tipo
  FROM tipo_boleta t
  WHERE t.id_tipo_boleta = i_id_tipo_boleta;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tipo_boleta_all()
RETURNS TABLE(
  id_tipo_boleta INT,
  tipo           VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_tipo_boleta, t.tipo
  FROM tipo_boleta t;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_tipo_boleta_by_id(
  i_id_tipo_boleta INT,
  i_tipo           VARCHAR,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE tipo_boleta
  SET tipo = i_tipo
  WHERE id_tipo_boleta = i_id_tipo_boleta;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del tipo de boleta ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en tipo de boleta table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;