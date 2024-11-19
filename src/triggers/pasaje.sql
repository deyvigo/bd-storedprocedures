CREATE TRIGGER IF NOT EXISTS update_occuped_seats
AFTER INSERT ON pasaje
FOR EACH ROW
BEGIN
UPDATE viaje_programado
SET asientos_ocupados = asientos_ocupados + 1
WHERE id_viaje_programado = NEW.id_viaje_programado;
END;