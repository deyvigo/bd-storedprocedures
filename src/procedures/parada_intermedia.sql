CREATE OR REPLACE PROCEDURE sp_register_parada_intermedia(
  i_ordinal              INT,
  i_id_terminal          INT,
  i_id_ruta              INT,
  OUT last_id            INT,
  OUT rows_affected      INT,
  OUT error_message      VARCHAR
) AS $$
BEGIN
  INSERT INTO parada_intermedia (ordinal, id_terminal, id_ruta)
  VALUES (i_ordinal, i_id_terminal, i_id_ruta)
  RETURNING id_parada_intermedia INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'La parada intermedia ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar la parada intermedia';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_parada_intermedia_by_id(i_id_parada_intermedia INT)
RETURNS TABLE(
  id_parada_intermedia INT,
  ordinal              INT,
  id_terminal          INT,
  id_ruta              INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id_parada_intermedia, p.ordinal, p.id_terminal, p.id_ruta
  FROM parada_intermedia p
  WHERE p.id_parada_intermedia = i_id_parada_intermedia;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_parada_intermedia_all()
RETURNS TABLE(
  id_parada_intermedia INT,
  ordinal              INT,
  id_terminal          INT,
  id_ruta              INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id_parada_intermedia, p.ordinal, p.id_terminal, p.id_ruta
  FROM parada_intermedia p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_parada_intermedia_by_id(
  i_id_parada_intermedia INT,
  i_ordinal              INT,
  i_id_terminal          INT,
  i_id_ruta              INT,
  OUT rows_affected       INT,
  OUT error_message       VARCHAR
) AS $$
BEGIN
  UPDATE parada_intermedia
  SET ordinal = i_ordinal,
      id_terminal = i_id_terminal,
      id_ruta = i_id_ruta
  WHERE id_parada_intermedia = i_id_parada_intermedia;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del parada intermedia ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en parada intermedia table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;