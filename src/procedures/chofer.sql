CREATE OR REPLACE PROCEDURE sp_register_chofer(
  nombre            VARCHAR,
  apellido_pat      VARCHAR,
  apellido_mat      VARCHAR,
  sexo              VARCHAR,
  OUT last_id       INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  INSERT INTO chofer (nombre, apellido_pat, apellido_mat, sexo)
  VALUES (nombre, apellido_pat, apellido_mat, sexo)
  RETURNING id_chofer INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El chofer ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el chofer';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_chofer_by_id(i_id_chofer INT)
RETURNS TABLE(
  id_chofer    INT,
  nombre       VARCHAR,
  apellido_pat VARCHAR,
  apellido_mat VARCHAR,
  sexo         VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT c.id_chofer, c.nombre, c.apellido_pat, c.apellido_mat, c.sexo
  FROM chofer c
  WHERE c.id_chofer = i_id_chofer;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_chofer_all()
RETURNS TABLE(
  id_chofer    INT,
  nombre       VARCHAR,
  apellido_pat VARCHAR,
  apellido_mat VARCHAR,
  sexo         VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT c.id_chofer, c.nombre, c.apellido_pat, c.apellido_mat, c.sexo
  FROM chofer c;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_chofer_by_id(
  i_id_chofer      INT,
  i_nombre         VARCHAR,
  i_apellido_pat   VARCHAR,
  i_apellido_mat   VARCHAR,
  i_sexo           VARCHAR,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE chofer
  SET nombre = i_nombre,
      apellido_pat = i_apellido_pat,
      apellido_mat = i_apellido_mat,
      sexo = i_sexo
  WHERE id_chofer = i_id_chofer;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del chofer ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en chofer table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;
