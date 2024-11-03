CREATE PROCEDURE IF NOT EXISTS sp_register_tipo_servicio_bus(
  IN  i_servicio             varchar(50),
  OUT last_id                int,
  OUT rows_affected          int,
  OUT error_message          varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el tipo de servicio de bus';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO tipo_servicio_bus (servicio) VALUES (i_servicio);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_tipo_servicio_bus_by_id(
  IN  i_id_tipo_servicio_bus int
)
BEGIN
  SELECT * FROM tipo_servicio_bus WHERE id_tipo_servicio_bus = i_id_tipo_servicio_bus;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_tipo_servicio_bus_all()
BEGIN
  SELECT * FROM tipo_servicio_bus;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_tipo_servicio_bus_by_id(
  IN  i_id_tipo_servicio_bus  int,
  IN  i_servicio              varchar(50),
  OUT rows_affected           int,
  OUT error_message           varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el tipo de servicio de bus';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE tipo_servicio_bus SET servicio = i_servicio WHERE id_tipo_servicio_bus = i_id_tipo_servicio_bus;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;