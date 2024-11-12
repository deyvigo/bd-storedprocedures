CREATE PROCEDURE IF NOT EXISTS sp_register_metodo_pago(
  IN  i_nombre            varchar(50),
  IN  i_numero_tarjeta    varchar(16),
  IN  i_id_cliente        int,
  OUT last_id             int,
  OUT rows_affected       int,
  OUT error_message       varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el metodo de pago';
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO metodo_pago (nombre, numero_tarjeta, id_cliente)
  VALUES (i_nombre, i_numero_tarjeta, i_id_cliente);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_metodo_pago_by_id(
  IN  i_id_metodo_pago int
)
BEGIN
  SELECT * FROM metodo_pago WHERE id_metodo_pago = i_id_metodo_pago;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_metodo_pago_all()
BEGIN
  SELECT * FROM metodo_pago;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_metodo_pago_by_id(
  IN  i_id_metodo_pago  int,
  IN  i_nombre          varchar(50),
  IN  i_numero_tarjeta  varchar(16),
  IN  i_id_cliente      int,
  OUT rows_affected     int,
  OUT error_message     varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el metodo de pago';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE metodo_pago
  SET nombre = i_nombre, numero_tarjeta = i_numero_tarjeta, fecha_vencimiento = i_fecha_vencimiento, id_cliente = i_id_cliente
  WHERE id_metodo_pago = i_id_metodo_pago;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;
