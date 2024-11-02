CREATE OR REPLACE FUNCTION get_admin_by_username(i_username VARCHAR)
RETURNS TABLE(
  id_admin         INT,
  nombre           VARCHAR,
  apellido_pat     VARCHAR,
  apellido_mat     VARCHAR,
  fecha_nacimiento DATE,
  dni              VARCHAR,
  sexo             VARCHAR,
  telefono         VARCHAR,
  correo           VARCHAR,
  username         VARCHAR,
  password         VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT a.id_admin, a.nombre, a.apellido_pat, a.apellido_mat, a.fecha_nacimiento, a.dni, a.sexo, a.telefono, a.correo, a.username, a.password
  FROM admin a
  WHERE a.username = i_username;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION register_admin(
  i_nombre           VARCHAR,
  i_apellido_pat     VARCHAR,
  i_apellido_mat     VARCHAR,
  i_fecha_nacimiento DATE,
  i_dni              VARCHAR,
  i_sexo             VARCHAR,
  i_telefono         VARCHAR,
  i_correo           VARCHAR,
  i_username         VARCHAR,
  i_password         VARCHAR
)
RETURNS TABLE(last_id INT, rows_affected INT) AS $$
DECLARE
  last_id INT;
  rows_affected INT;
BEGIN
  INSERT INTO admin (nombre, apellido_pat, apellido_mat, fecha_nacimiento, dni, sexo, telefono, correo, username, password)
  VALUES (i_nombre, i_apellido_pat, i_apellido_mat, i_fecha_nacimiento, i_dni, i_sexo, i_telefono, i_correo, i_username, i_password)
  RETURNING id_admin INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;

  RETURN QUERY SELECT last_id, rows_affected;
END;
$$ LANGUAGE plpgsql;

