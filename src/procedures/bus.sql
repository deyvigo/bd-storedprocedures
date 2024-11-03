CREATE OR REPLACE PROCEDURE sp_register_bus(
  i_asientos             INT,
  i_placa                VARCHAR,
  i_marca                VARCHAR,
  i_niveles              INT,
  i_id_tipo_servicio_bus INT,
  OUT last_id            INT,
  OUT rows_affected      INT,
  OUT error_message      VARCHAR
) AS $$
BEGIN
  INSERT INTO bus (asientos, placa, marca, niveles, id_tipo_servicio_bus)
  VALUES (i_asientos, i_placa, i_marca, i_niveles, i_id_tipo_servicio_bus)
  RETURNING id_bus INTO last_id;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'El bus ya existe';
    last_id := NULL;
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error al registrar el bus';
    last_id := NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_bus_by_id(i_id_bus INT)
RETURNS TABLE(
  id_bus               INT,
  asientos             INT,
  placa                VARCHAR,
  marca                VARCHAR,
  niveles              INT,
  id_tipo_servicio_bus INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT b.id_bus, b.asientos, b.placa, b.marca, b.niveles, b.id_tipo_servicio_bus
  FROM bus b
  WHERE b.id_bus = i_id_bus;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_bus_all()
RETURNS TABLE(
  id_bus               INT,
  asientos             INT,
  placa                VARCHAR,
  marca                VARCHAR,
  niveles              INT,
  id_tipo_servicio_bus INT
) AS $$
BEGIN
  RETURN QUERY
  SELECT b.id_bus, b.asientos, b.placa, b.marca, b.niveles, b.id_tipo_servicio_bus
  FROM bus b;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE sp_update_bus_by_id(
  i_id_bus              INT,
  i_asientos            INT,
  i_placa               VARCHAR,
  i_marca               VARCHAR,
  i_niveles             INT,
  i_id_tipo_servicio_bus INT,
  OUT rows_affected      INT,
  OUT error_message      VARCHAR
) AS $$
BEGIN
  UPDATE bus
  SET asientos = i_asientos,
      placa = i_placa,
      marca = i_marca,
      niveles = i_niveles,
      id_tipo_servicio_bus = i_id_tipo_servicio_bus
  WHERE id_bus = i_id_bus;

  GET DIAGNOSTICS rows_affected = ROW_COUNT;
  error_message := NULL;

EXCEPTION
  WHEN unique_violation THEN
    rows_affected := 0;
    error_message := 'Alguno de los campos del bus ya existe';
    
  WHEN OTHERS THEN
    rows_affected := 0;
    error_message := 'Error desconocido en bus table' || SQLERRM;
END;
$$ LANGUAGE plpgsql;