CREATE OR REPLACE PROCEDURE sp_register_asiento(
  i_nivel            INT,
  i_numero           INT,
  i_id_bus           INT,
  OUT last_id        INT,
  OUT rows_affected  INT,
  OUT error_message  VARCHAR
) AS $$
BEGIN
  INSERT INTO asiento (nivel, numero, id_bus)
  VALUES (i_nivel, i_numero, i_id_bus)
  RETURNING id_asiento INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El asiento ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el asiento';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_asiento_by_id(i_id_asiento INT)
RETURNS TABLE(
  id_asiento INT,
  nivel      INT,
  numero     INT,
  id_bus     INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT a.id_asiento, a.nivel, a.numero, a.id_bus
  FROM asiento a
  WHERE a.id_asiento = i_id_asiento;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_asiento_all()
RETURNS TABLE(
  id_asiento INT,
  nivel      INT,
  numero     INT,
  id_bus     INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT a.id_asiento, a.nivel, a.numero, a.id_bus
  FROM asiento a;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_asiento_by_id(
  i_id_asiento      INT,
  i_nivel           INT,
  i_numero          INT,
  i_id_bus          INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE asiento
  SET nivel = i_nivel,
      numero = i_numero,
      id_bus = i_id_bus
  WHERE id_asiento = i_id_asiento;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del asiento ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en asiento table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;