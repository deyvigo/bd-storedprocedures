CREATE OR REPLACE PROCEDURE sp_register_pasajero(
  i_dni              VARCHAR,
  i_nombre           VARCHAR,
  i_apellido_pat     VARCHAR,
  i_apellido_mat     VARCHAR,
  i_fecha_nacimiento DATE,
  i_sexo             VARCHAR,
  OUT last_id         INT,
  OUT rows_affected   INT,
  OUT error_message   VARCHAR
) AS $$
BEGIN
  INSERT INTO pasajero (dni, nombre, apellido_pat, apellido_mat, fecha_nacimiento, sexo)
  VALUES (i_dni, i_nombre, i_apellido_pat, i_apellido_mat, i_fecha_nacimiento, i_sexo)
  RETURNING id_pasajero INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El pasajero ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar al pasajero';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_pasajero_by_id(i_id_pasajero INT)
RETURNS TABLE(
  id_pasajero      INT,
  dni              VARCHAR,
  nombre           VARCHAR,
  apellido_pat     VARCHAR,
  apellido_mat     VARCHAR,
  fecha_nacimiento DATE,
  sexo             VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id_pasajero, p.dni, p.nombre, p.apellido_pat, p.apellido_mat, p.fecha_nacimiento, p.sexo
  FROM pasajero p
  WHERE p.id_pasajero = i_id_pasajero;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_pasajero_all()
RETURNS TABLE(
  id_pasajero      INT,
  dni              VARCHAR,
  nombre           VARCHAR,
  apellido_pat     VARCHAR,
  apellido_mat     VARCHAR,
  fecha_nacimiento DATE,
  sexo             VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT p.id_pasajero, p.dni, p.nombre, p.apellido_pat, p.apellido_mat, p.fecha_nacimiento, p.sexo
  FROM pasajero p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_pasajero_by_id(
  i_id_pasajero    INT,
  i_dni            VARCHAR,
  i_nombre         VARCHAR,
  i_apellido_pat   VARCHAR,
  i_apellido_mat   VARCHAR,
  i_fecha_nacimiento DATE,
  i_sexo           VARCHAR,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE pasajero
  SET dni = i_dni,
      nombre = i_nombre,
      apellido_pat = i_apellido_pat,
      apellido_mat = i_apellido_mat,
      fecha_nacimiento = i_fecha_nacimiento,
      sexo = i_sexo
  WHERE id_pasajero = i_id_pasajero;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del pasajero ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en pasajero table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;