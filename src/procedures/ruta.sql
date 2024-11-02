CREATE OR REPLACE PROCEDURE sp_register_ruta(
  i_duracion_estimada INTERVAL,
  i_distancia         DOUBLE PRECISION,
  i_estado            VARCHAR,
  i_id_origen         INT,
  i_id_destino        INT,
  OUT last_id         INT,
  OUT rows_affected   INT,
  OUT error_message   VARCHAR
) AS $$
BEGIN
  INSERT INTO ruta (duracion_estimada, distancia, estado, id_origen, id_destino)
  VALUES (i_duracion_estimada, i_distancia, i_estado, i_id_origen, i_id_destino)
  RETURNING id_ruta INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'La ruta ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar la ruta';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_ruta_by_id(i_id_ruta INT)
RETURNS TABLE(
  id_ruta           INT,
  duracion_estimada INTERVAL,
  distancia         DOUBLE PRECISION,
  estado            VARCHAR,
  id_origen         INT,
  id_destino        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT r.id_ruta, r.duracion_estimada, r.distancia, r.estado, r.id_origen, r.id_destino
  FROM ruta r
  WHERE r.id_ruta = i_id_ruta;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_ruta_all()
RETURNS TABLE(
  id_ruta           INT,
  duracion_estimada INTERVAL,
  distancia         DOUBLE PRECISION,
  estado            VARCHAR,
  id_origen         INT,
  id_destino        INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT r.id_ruta, r.duracion_estimada, r.distancia, r.estado, r.id_origen, r.id_destino
  FROM ruta r;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_ruta_by_id(
  i_id_ruta         INT,
  i_duracion_estimada INTERVAL,
  i_distancia       DOUBLE PRECISION,
  i_estado          VARCHAR,
  i_id_origen       INT,
  i_id_destino      INT,
  OUT rows_affected INT,
  OUT error_message VARCHAR
) AS $$
BEGIN
  UPDATE ruta
  SET duracion_estimada = i_duracion_estimada,
      distancia = i_distancia,
      estado = i_estado,
      id_origen = i_id_origen,
      id_destino = i_id_destino
  WHERE id_ruta = i_id_ruta;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos de la ruta ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en ruta table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;