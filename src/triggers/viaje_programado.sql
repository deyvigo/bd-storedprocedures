CREATE TRIGGER IF NOT EXISTS tgr_verify_chofer
BEFORE INSERT ON viaje_programado
FOR EACH ROW
BEGIN
    DECLARE chofer_despedido INT;
    SELECT COUNT(1) INTO chofer_despedido
    FROM chofer
    WHERE id_chofer = NEW.id_chofer AND estado = 'despedido';

    IF chofer_despedido > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El chofer está despedido';
    END IF;
END