CREATE OR REPLACE PROCEDURE sp_register_terminal(
  i_nombre       VARCHAR,
  i_departamento VARCHAR,
  i_provincia    VARCHAR,
  OUT last_id    INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  INSERT INTO terminal (nombre, departamento, provincia)
  VALUES (i_nombre, i_departamento, i_provincia)
  RETURNING id_terminal INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'La terminal ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar la terminal';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_terminal_by_id(i_id_terminal INT)
RETURNS TABLE(
  id_terminal  INT,
  nombre       VARCHAR,
  departamento VARCHAR,
  provincia    VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_terminal, t.nombre, t.departamento, t.provincia
  FROM terminal t
  WHERE t.id_terminal = i_id_terminal;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_terminal_all()
RETURNS TABLE(
  id_terminal  INT,
  nombre       VARCHAR,
  departamento VARCHAR,
  provincia    VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_terminal, t.nombre, t.departamento, t.provincia
  FROM terminal t;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_terminal_by_id(
  i_id_terminal  INT,
  i_nombre       VARCHAR,
  i_departamento VARCHAR,
  i_provincia    VARCHAR,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE terminal
  SET nombre = i_nombre,
      departamento = i_departamento,
      provincia = i_provincia
  WHERE id_terminal = i_id_terminal;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del terminal ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en terminal table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;