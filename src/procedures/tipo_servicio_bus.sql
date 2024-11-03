CREATE OR REPLACE PROCEDURE sp_register_tipo_servicio_bus(
  i_servicio             VARCHAR,
  OUT last_id            INT,
  OUT rows_affected      INT,
  OUT error_message      VARCHAR
) AS $$
BEGIN
  INSERT INTO tipo_servicio_bus (servicio)
  VALUES (i_servicio)
  RETURNING id_tipo_servicio_bus INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El tipo de servicio de bus ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el tipo de servicio de bus';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tipo_servicio_bus_by_id(i_id_tipo_servicio_bus INT)
RETURNS TABLE(
  id_tipo_servicio_bus INT,
  servicio             VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_tipo_servicio_bus, t.servicio
  FROM tipo_servicio_bus t
  WHERE t.id_tipo_servicio_bus = i_id_tipo_servicio_bus;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_tipo_servicio_bus_all()
RETURNS TABLE(
  id_tipo_servicio_bus INT,
  servicio             VARCHAR
) AS $$
BEGIN
  RETURN QUERY
  SELECT t.id_tipo_servicio_bus, t.servicio
  FROM tipo_servicio_bus t;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_tipo_servicio_bus_by_id(
  i_id_tipo_servicio_bus  INT,
  i_servicio              VARCHAR,
  OUT rows_affected       INT,
  OUT error_message       VARCHAR
) AS $$
BEGIN
  UPDATE tipo_servicio_bus
  SET servicio = i_servicio
  WHERE id_tipo_servicio_bus = i_id_tipo_servicio_bus;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del tipo de servicio de bus ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en tipo de servicio de bus table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;