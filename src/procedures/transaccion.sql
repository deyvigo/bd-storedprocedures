CREATE PROCEDURE IF NOT EXISTS sp_register_transaccion(
  IN  i_precio_neto       decimal(8, 2),
  IN  i_igv               decimal(8, 2),
  IN  i_precio_total      decimal(8, 2),
  IN  i_fecha_compra      datetime,
  IN  i_ruc               varchar(20),
  IN  i_correo_contacto   varchar(255),
  IN  i_telefono_contacto varchar(20),
  IN  i_id_cliente        int,
  IN  i_id_descuento      int,
  IN  i_id_tipo_boleta    int,
  IN  i_id_metodo_pago    int,
  OUT last_id             int,
  OUT rows_affected       int,
  OUT error_message       varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    GET DIAGNOSTICS CONDITION 1
      error_message = MESSAGE_TEXT;
    SET rows_affected = -1;
    SET last_id = -1;
    ROLLBACK;
  END;
  
  START TRANSACTION;
  INSERT INTO transaccion (precio_neto, igv, precio_total, fecha_compra, ruc, correo_contacto, telefono_contacto, id_cliente, id_descuento, id_tipo_boleta, id_metodo_pago)
  VALUES (i_precio_neto, i_igv, i_precio_total, i_fecha_compra, i_ruc, i_correo_contacto, i_telefono_contacto, i_id_cliente, i_id_descuento, i_id_tipo_boleta, i_id_metodo_pago);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_transaccion_by_id(
  IN  i_id_transaccion int
)
BEGIN
  SELECT * FROM transaccion WHERE id_transaccion = i_id_transaccion;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_transaccion_all()
BEGIN
  SELECT * FROM transaccion;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_transaccion_by_id(
  IN  i_id_transaccion    int,
  IN  i_precio_neto       decimal(8, 2),
  IN  i_igv               decimal(8, 2),
  IN  i_precio_total      decimal(8, 2),
  IN  i_fecha_compra      timestamp,
  IN  i_ruc               varchar(20),
  IN  i_correo_contacto   varchar(255),
  IN  i_telefono_contacto varchar(20),
  IN  i_id_cliente        int,
  IN  i_id_descuento      int,
  IN  i_id_tipo_boleta    int,
  IN  i_id_metodo_pago    int,
  OUT rows_affected       int,
  OUT error_message       varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar la transaccion';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE transaccion
  SET precio_neto = i_precio_neto, igv = i_igv, precio_total = i_precio_total, fecha_compra = i_fecha_compra, ruc = i_ruc, correo_contacto = i_correo_contacto, telefono_contacto = i_telefono_contacto, id_cliente = i_id_cliente, id_descuento = i_id_descuento, id_tipo_boleta = i_id_tipo_boleta, id_metodo_pago = i_id_metodo_pago
  WHERE id_transaccion = i_id_transaccion;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_transaccion_by_id_cliente(
  IN  i_id_cliente int
)
BEGIN
  SELECT tr.id_transaccion, tr.fecha_compra, tr.precio_total, COUNT(p.id_transaccion) AS cantidad_pasajes
  FROM transaccion tr
  JOIN pasaje p ON p.id_transaccion = tr.id_transaccion
  WHERE tr.id_cliente = i_id_cliente
  GROUP BY tr.id_transaccion
  ORDER BY tr.fecha_compra ASC;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_transaccion_by_id(
  IN  i_id_transaccion int
)
BEGIN
  SELECT
    tr.id_transaccion,
    tr.fecha_compra,
    tr.precio_total,
    COUNT(p.id_pasaje) AS cantidad_pasajes,
    tr.igv,
    tr.ruc,
    tr.precio_neto
  FROM transaccion tr
  WHERE tr.id_transaccion = i_id_transaccion;
END;