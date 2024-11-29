CREATE PROCEDURE IF NOT EXISTS sp_register_terminal(
  IN  i_nombre       varchar(255),
  IN  i_departamento varchar(100),
  IN  i_provincia    varchar(100),
  OUT last_id        int,
  OUT rows_affected  int,
  OUT error_message  varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar registrar la terminal';
    SET last_id = -1;
    ROLLBACK;
  END;

  START TRANSACTION;
  INSERT INTO terminal (nombre, departamento, provincia)
  VALUES (i_nombre, i_departamento, i_provincia);
  SET rows_affected = ROW_COUNT();
  SET last_id = LAST_INSERT_ID();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_terminal_by_id(
  IN  i_id_terminal int
)
BEGIN
  SELECT * FROM terminal WHERE id_terminal = i_id_terminal;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_terminal_all()
BEGIN
  SELECT * FROM terminal;
END;

CREATE PROCEDURE IF NOT EXISTS sp_update_terminal_by_id(
  IN  i_id_terminal  int,
  IN  i_nombre       varchar(255),
  IN  i_departamento varchar(100),
  IN  i_provincia    varchar(100),
  OUT rows_affected  int,
  OUT error_message  varchar(255)
)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    SET rows_affected = -1;
    SET error_message = 'Error al intentar actualizar la terminal';
    ROLLBACK;
  END;
  
  START TRANSACTION;
  UPDATE terminal
  SET nombre = i_nombre, departamento = i_departamento, provincia = i_provincia
  WHERE id_terminal = i_id_terminal;
  SET rows_affected = ROW_COUNT();
  SET error_message = NULL;
  COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS sp_get_departamento_terminal()
BEGIN 
  SELECT 
    ROW_NUMBER() OVER () AS id,
    departamento
  FROM (
    SELECT departamento
    FROM terminal
    GROUP BY departamento
  ) AS subquery;
END;
