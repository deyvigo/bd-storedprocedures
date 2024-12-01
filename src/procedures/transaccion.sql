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

CREATE PROCEDURE IF NOT EXISTS sp_get_transaccion_by_id_for_pdf(
  IN  i_id_transaccion int
)
BEGIN
  SELECT
    tr.id_transaccion,
    tr.fecha_compra,
    tr.precio_total,
    COUNT(p.id_pasaje) AS cantidad_pasajes,
    t_origen.departamento AS origen,
    t_destino.departamento AS destino,
    tsb.servicio,
    c.dni,
    tr.igv,
    tr.ruc,
    tr.precio_neto,
    COALESCE(d.monto, 0) AS descuento,
    mp.numero_tarjeta
  FROM transaccion tr
  JOIN pasaje p ON p.id_transaccion = tr.id_transaccion
  JOIN cliente c ON c.id_cliente = tr.id_cliente
  LEFT JOIN descuento d ON d.id_descuento = tr.id_descuento
  JOIN metodo_pago mp ON mp.id_metodo_pago = tr.id_metodo_pago
  JOIN viaje_programado vp ON vp.id_viaje_programado = p.id_viaje_programado
  JOIN ruta r ON r.id_ruta = vp.id_ruta
  JOIN terminal t_origen ON t_origen.id_terminal = r.id_origen
  JOIN terminal t_destino ON t_destino.id_terminal = r.id_destino
  JOIN bus b ON b.id_bus = vp.id_bus
  JOIN tipo_servicio_bus tsb ON tsb.id_tipo_servicio_bus = b.id_tipo_servicio_bus
  WHERE tr.id_transaccion = i_id_transaccion;
END;


CREATE PROCEDURE IF NOT EXISTS sp_register_transaction_with_tickets(
  IN i_precio_neto DECIMAL(8, 2),
  IN i_igv DECIMAL(8, 2),
  IN i_precio_total DECIMAL(8, 2),
  IN i_fecha_compra DATETIME,
  IN i_ruc VARCHAR(20),
  IN i_correo_contacto VARCHAR(255),
  IN i_telefono_contacto VARCHAR(20),
  IN i_id_cliente INT,
  IN i_id_descuento INT,
  IN i_id_tipo_boleta INT,
  IN i_id_metodo_pago INT,
  IN pasajes_data JSON,
  OUT error_message VARCHAR(255)
)
BEGIN
  DECLARE last_transaccion_id INT;
  DECLARE rows_affected INT DEFAULT 0;
  DECLARE last_pasaje_id INT;
  DECLARE pasaje_rows_affected INT DEFAULT 0;

  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    -- Capturar el estado SQL y el mensaje de error
    GET DIAGNOSTICS CONDITION 1 @sqlstate = RETURNED_SQLSTATE, @message = MESSAGE_TEXT;
    SET error_message = CONCAT('Error: ', @sqlstate, ' - ', @message);
    ROLLBACK;
  END;

  -- Iniciar transacción
  START TRANSACTION;

  -- Etiqueta para el bloque principal
  main_loop: BEGIN

    -- Registrar transacción
    CALL sp_register_transaccion(
      i_precio_neto, i_igv, i_precio_total, i_fecha_compra,
      i_ruc, i_correo_contacto, i_telefono_contacto, i_id_cliente,
      i_id_descuento, i_id_tipo_boleta, i_id_metodo_pago,
      last_transaccion_id, rows_affected, error_message
    );

    -- Verificar transacción exitosa
    IF rows_affected <= 0 THEN
      ROLLBACK;
      LEAVE main_loop; -- Salir del bloque principal
    END IF;

    -- Registrar pasajes
    SET @precio_total_transaccion = 0.00;
    SET @precio_neto_transaccion = 0.00;
    SET @igv_transaccion = 0.00;
    SET @index = 0;
    SET @total_pasajes = JSON_LENGTH(pasajes_data);

    WHILE @index < @total_pasajes DO
      CALL sp_register_pasaje(
        i_fecha_compra,
        JSON_UNQUOTE(JSON_EXTRACT(pasajes_data, CONCAT('$[', @index, '].precio_neto'))),
        JSON_UNQUOTE(JSON_EXTRACT(pasajes_data, CONCAT('$[', @index, '].igv'))),
        JSON_UNQUOTE(JSON_EXTRACT(pasajes_data, CONCAT('$[', @index, '].precio_total'))),
        JSON_UNQUOTE(JSON_EXTRACT(pasajes_data, CONCAT('$[', @index, '].id_pasajero'))),
        JSON_UNQUOTE(JSON_EXTRACT(pasajes_data, CONCAT('$[', @index, '].id_asiento'))),
        JSON_UNQUOTE(JSON_EXTRACT(pasajes_data, CONCAT('$[', @index, '].id_viaje_programado'))),
        last_transaccion_id,
        NULL, -- Fecha de modificación
        NULL,              -- ID admin mod
        last_pasaje_id,
        pasaje_rows_affected,
        error_message
      );

      -- Validar pasaje
      IF pasaje_rows_affected <= 0 THEN
        SET error_message = 'Error al registrar el pasaje.';
        ROLLBACK;
        LEAVE main_loop; -- Salir del bloque principal
      END IF;

      SET @index = @index + 1;
    END WHILE;

    -- Finalizar transacción
    COMMIT;
    SET error_message = NULL; -- Indicar que no hubo errores

  END main_loop; -- Fin del bloque principal

END

