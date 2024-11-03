CREATE PROCEDURE IF NOT EXISTS sp_register_bus(
  IN  i_asientos             int,
  IN  i_placa                varchar(7),
  IN  i_marca                varchar(50),
  IN  i_niveles              int,
  IN  i_id_tipo_servicio_bus int,
  OUT last_id                int,
  OUT rows_affected          int,
  OUT error_message          varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el bus';
    SET last_id = -1;
    ROLLBACK;
  END;

  START TRANSACTION;
  INSERT INTO bus (asientos, placa, marca, niveles, id_tipo_servicio_bus)
  VALUES (i_asientos, i_placa, i_marca, i_niveles, i_id_tipo_servicio_bus);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_bus_by_id(
  IN  i_id_bus int
)
BEGIN
  SELECT * FROM bus WHERE id_bus = i_id_bus;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_bus_all()
BEGIN
  SELECT * FROM bus;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_bus_by_id(
  IN  i_id_bus              int,
  IN  i_asientos            int,
  IN  i_placa               varchar(7),
  IN  i_marca               varchar(50),
  IN  i_niveles             int,
  IN  i_id_tipo_servicio_bus int,
  OUT rows_affected          int,
  OUT error_message          varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el bus';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE bus
  SET asientos = i_asientos, placa = i_placa, marca = i_marca, niveles = i_niveles, id_tipo_servicio_bus = i_id_tipo_servicio_bus
  WHERE id_bus = i_id_bus;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;