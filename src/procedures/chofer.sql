CREATE OR REPLACE PROCEDURE sp_register_chofer(
  nombre            VARCHAR,
  apellido_pat      VARCHAR,
  apellido_mat      VARCHAR,
  sexo              VARCHAR,
  dni               VARCHAR,
  OUT last_id       INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  INSERT INTO chofer (nombre, apellido_pat, apellido_mat, sexo, dni)
  VALUES (nombre, apellido_pat, apellido_mat, sexo, dni)
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
    error_message := 'Error al registrar el chofer ' || SQLERRM;
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


CREATE OR REPLACE PROCEDURE sp_update_status_chofer_by_id(
  IN i_id_chofer INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR(255)
)
LANGUAGE plpgsql
AS $$
BEGIN
  BEGIN
      UPDATE chofer
      SET estado = CASE
                    WHEN estado = 'contratado' THEN 'despedido'
                    WHEN estado = 'despedido' THEN 'contratado'
                  END
      WHERE id_chofer = i_id_chofer;
      
      GET DIAGNOSTICS rows_affected = ROW_COUNT;
      error_message := NULL;
  EXCEPTION
      WHEN OTHERS THEN
          rows_affected := -1;
          error_message := 'Error al intentar actualizar el chofer';
  END;
END;

CREATE OR REPLACE FUNCTION sp_get_free_chofer(i_date DATE)
RETURNS TABLE (
    id_chofer INT,
    nombre VARCHAR,
    apellido_pat VARCHAR,
    apellido_mat VARCHAR,
    dni VARCHAR,
    sexo VARCHAR,
    estado VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT chofer.*
    FROM chofer
    LEFT JOIN viaje_programado 
    ON chofer.id_chofer = viaje_programado.id_chofer 
    AND viaje_programado.fecha_salida BETWEEN i_date AND i_date + INTERVAL '1 day'
    WHERE chofer.estado = 'contratado'
    AND viaje_programado.id_chofer IS NULL;
END;
$$;

CREATE OR REPLACE FUNCTION sp_get_hired_chofer()
RETURNS TABLE (
    id_chofer INT,
    nombre VARCHAR,
    apellido_pat VARCHAR,
    apellido_mat VARCHAR,
    dni VARCHAR,
    sexo VARCHAR,
    estado VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM chofer WHERE estado = 'contratado';
END;
$$;

CREATE OR REPLACE FUNCTION sp_get_fired_chofer()
RETURNS TABLE (
    id_chofer INT,
    nombre VARCHAR,
    apellido_pat VARCHAR,
    apellido_mat VARCHAR,
    dni VARCHAR,
    sexo VARCHAR,
    estado VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM chofer WHERE estado = 'despedido';
END;
$$;

CREATE OR REPLACE PROCEDURE sp_update_chofer_by_id(
    i_id_chofer INT,
    i_nombre VARCHAR(255),
    i_apellido_pat VARCHAR(50),
    i_apellido_mat VARCHAR(50),
    i_dni VARCHAR(8),
    i_sexo VARCHAR(15),
    OUT rows_affected INT,
    OUT error_message VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    BEGIN
        UPDATE chofer
        SET 
            nombre = i_nombre,
            apellido_pat = i_apellido_pat,
            apellido_mat = i_apellido_mat,
            dni = i_dni,
            sexo = i_sexo
        WHERE id_chofer = i_id_chofer;

        rows_affected := FOUND::INT; 
        error_message := NULL;
    EXCEPTION
        WHEN OTHERS THEN
            rows_affected := -1;
            error_message := 'Error al intentar actualizar el chofer';
    END;
END;
$$;
