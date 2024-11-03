CREATE PROCEDURE IF NOT EXISTS sp_register_descuento(
  IN  i_codigo          varchar(30),
  IN  i_monto           decimal(8, 2),
  IN  i_estado          varchar(20),
  IN  i_id_admin        int,
  OUT last_id           int,
  OUT rows_affected     int,
  OUT error_message     varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar el descuento';
    SET last_id = -1;
    ROLLBACK;
  END;

  START TRANSACTION;
  INSERT INTO descuento (codigo, monto, estado, id_admin)
  VALUES (i_codigo, i_monto, i_estado, i_id_admin);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_descuento_by_id(
  IN  i_id_descuento int
)
BEGIN
  SELECT * FROM descuento WHERE id_descuento = i_id_descuento;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_descuento_all()
BEGIN
  SELECT * FROM descuento;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_descuento_by_id(
  IN  i_id_descuento   int,
  IN  i_codigo         varchar(30),
  IN  i_monto          decimal(8, 2),
  IN  i_estado         varchar(20),
  IN  i_id_admin       int,
  OUT rows_affected    int,
  OUT error_message    varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar el descuento';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE descuento
  SET codigo = i_codigo, monto = i_monto, estado = i_estado, id_admin = i_id_admin
  WHERE id_descuento = i_id_descuento;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;
