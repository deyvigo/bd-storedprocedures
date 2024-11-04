CREATE PROCEDURE IF NOT EXISTS sp_get_destinos_by_city(
    IN  i_departamento varchar(100)
)
BEGIN
    SELECT DISTINCT t_destino.departamento AS Destinos 
    FROM ruta r
    INNER JOIN terminal t_origen ON r.id_origen = t_origen.id_terminal
    INNER JOIN terminal t_destino ON r.id_destino = t_destino.id_terminal
    WHERE t_origen.departamento = i_departamento;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_scheduled_trip(
    IN  i_origen varchar(100),
    IN  i_destino varchar(100),
    IN  i_fecha date
)
BEGIN
    SELECT 
        t_origen.nombre AS origen, 
        t_destino.nombre AS destino, 
        tsb.tipo_servicio AS servicio, 
        vp.fecha_salida AS fecha_salida, 
        vp.hora_salida AS hora_salida, 
        (vp.hora_salida+r.duracion_estimada) AS hora_llegada,
        vp.minutos_salida AS duracion, 
        vp.precio_nivel_uno AS precio_min, 
        (b.asientos-vp.asientos_ocupados) AS asientos_disponibles, 
        r.duracion_estimada AS duracion, r.distancia AS distancia 
    FROM viaje_programado vp
    INNER JOIN BUS b ON vp.id_bus = b.id_bus
    INNER JOIN ruta r ON vp.id_ruta = r.id_ruta
    INNER JOIN terminal t_origen ON r.id_origen = t_origen.id_terminal
    INNER JOIN terminal t_destino ON r.id_destino = t_destino.id_terminal
    INNER JOIN tipo_servicio_bus tsb ON b.id_tipo_servicio_bus = tsb.id_tipo_servicio_bus
    WHERE t_origen.departamento = i_origen
    AND t_destino.departamento = i_destino
    AND vp.fecha_salida = i_fecha
    AND (ab.asientos-vp.asientos_ocupados) > 0;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_seat_by_trip(
    IN  i_id_viaje_programado INT
)
BEGIN
    SELECT 
        a.id_asiento,
        a.nivel,
        a.numero,
        IF(p.id_pasaje IS NULL, 'Disponible', 'Ocupado') AS estado
    FROM asiento a
    LEFT JOIN pasaje p ON a.id_asiento = p.id_asiento 
    AND p.id_viaje_programado = i_id_viaje_programado
    WHERE 
        a.id_bus = (SELECT id_bus FROM viaje_programado WHERE id_viaje_programado = i_id_viaje_programado);
END;
