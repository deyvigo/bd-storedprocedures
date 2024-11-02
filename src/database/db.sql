CREATE TABLE IF NOT EXISTS admin
(
  id_admin         serial PRIMARY KEY,
  nombre           varchar(255) NOT NULL,
  apellido_pat     varchar(50)  NOT NULL,
  apellido_mat     varchar(50)  NOT NULL,
  fecha_nacimiento date         NOT NULL,
  dni              varchar(8)   NOT NULL,
  sexo             varchar(15)  NOT NULL,
  telefono         varchar(20)  NOT NULL,
  correo           varchar(255) NOT NULL UNIQUE,
  username         varchar(50)  NOT NULL UNIQUE,
  password         varchar(80)  NOT NULL
);

CREATE TABLE IF NOT EXISTS chofer
(
  id_chofer    serial PRIMARY KEY,
  nombre       varchar(255) NOT NULL,
  apellido_pat varchar(50)  NOT NULL,
  apellido_mat varchar(50)  NOT NULL,
  sexo         varchar(15)  NOT NULL
);

CREATE TABLE IF NOT EXISTS cliente
(
  id_cliente       serial PRIMARY KEY,
  dni              varchar(8)   NOT NULL,
  nombre           varchar(255) NOT NULL,
  apellido_pat     varchar(50)  NOT NULL,
  apellido_mat     varchar(50)  NOT NULL,
  fecha_nacimiento date         NOT NULL,
  sexo             varchar(15)  NOT NULL,
  telefono         varchar(20)  NOT NULL,
  correo           varchar(100) NOT NULL UNIQUE,
  username         varchar(50)  NOT NULL UNIQUE,
  password         varchar(80)  NOT NULL
);

CREATE TABLE IF NOT EXISTS descuento
(
  id_descuento serial PRIMARY KEY,
  codigo       varchar(30)   NOT NULL,
  monto        decimal(8, 2) NOT NULL,
  estado       varchar(20)   NOT NULL,
  id_admin     int           NOT NULL,
  CONSTRAINT descuento_admin_id_admin_fk
    FOREIGN KEY (id_admin) REFERENCES admin (id_admin)
);

CREATE TABLE IF NOT EXISTS metodo_pago
(
  id_metodo_pago    serial PRIMARY KEY,
  metodo            varchar(50) NOT NULL,
  numero_tarjeta    varchar(16) NOT NULL,
  cvv               varchar(3)  NOT NULL,
  fecha_vencimiento varchar(5)  NOT NULL,
  id_cliente        int         NOT NULL
);

CREATE TABLE IF NOT EXISTS pasajero
(
  id_pasajero      serial PRIMARY KEY,
  dni              varchar(8)   NOT NULL,
  nombre           varchar(255) NOT NULL,
  apellido_pat     varchar(50)  NOT NULL,
  apellido_mat     varchar(50)  NOT NULL,
  fecha_nacimiento date         NOT NULL,
  sexo             varchar(15)  NOT NULL
);

CREATE TABLE IF NOT EXISTS terminal
(
  id_terminal  serial PRIMARY KEY,
  nombre       varchar(255) NOT NULL,
  departamento varchar(100) NOT NULL,
  provincia    varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS parada_intermedia
(
  id_parada_intermedia serial PRIMARY KEY,
  ordinal              int NOT NULL,
  id_terminal          int NOT NULL,
  id_ruta              int NOT NULL,
  CONSTRAINT parada_intermedia_terminal_id_terminal_fk
    FOREIGN KEY (id_terminal) REFERENCES terminal (id_terminal)
);

CREATE TABLE IF NOT EXISTS ruta
(
  id_ruta           serial PRIMARY KEY,
  duracion_estimada interval     NOT NULL,
  distancia         double precision NOT NULL,
  estado            varchar(20)  NOT NULL,
  id_origen         int          NOT NULL,
  id_destino        int          NOT NULL,
  CONSTRAINT ruta_terminal_id_terminal_fk
    FOREIGN KEY (id_origen) REFERENCES terminal (id_terminal),
  CONSTRAINT ruta_terminal_id_terminal_fk_2
    FOREIGN KEY (id_destino) REFERENCES terminal (id_terminal)
);

CREATE TABLE IF NOT EXISTS tipo_boleta
(
  id_tipo_boleta serial PRIMARY KEY,
  tipo           varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_servicio_bus
(
  id_tipo_servicio_bus serial PRIMARY KEY,
  servicio             varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS bus
(
  id_bus               serial PRIMARY KEY,
  asientos             int         NOT NULL,
  placa                varchar(7)  NOT NULL,
  marca                varchar(50) NOT NULL,
  niveles              int         NOT NULL,
  id_tipo_servicio_bus int         NOT NULL,
  CONSTRAINT bus_tipo_servicio_bus_id_tipo_servicio_bus_fk
    FOREIGN KEY (id_tipo_servicio_bus) REFERENCES tipo_servicio_bus (id_tipo_servicio_bus)
);

CREATE TABLE IF NOT EXISTS asiento
(
  id_asiento serial PRIMARY KEY,
  nivel      int NOT NULL,
  numero     int NOT NULL,
  id_bus     int NOT NULL,
  CONSTRAINT asiento_bus_id_bus_fk
    FOREIGN KEY (id_bus) REFERENCES bus (id_bus)
);

CREATE TABLE IF NOT EXISTS transaccion
(
  id_transaccion    serial PRIMARY KEY,
  precio_neto       decimal(8, 2) NOT NULL,
  igv               decimal(8, 2) NOT NULL,
  precio_total      decimal(8, 2) NOT NULL,
  fecha_compra      timestamp     NOT NULL,
  ruc               varchar(20)   NULL,
  correo_contacto   varchar(255)  NOT NULL,
  telefono_contacto varchar(20)   NOT NULL,
  id_cliente        int           NOT NULL,
  id_descuento      int           NOT NULL,
  id_tipo_boleta    int           NOT NULL,
  CONSTRAINT transaccion_cliente_id_cliente_fk
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente),
  CONSTRAINT transaccion_descuento_id_descuento_fk
    FOREIGN KEY (id_descuento) REFERENCES descuento (id_descuento),
  CONSTRAINT transaccion_tipo_boleta_id_tipo_boleta_fk
    FOREIGN KEY (id_tipo_boleta) REFERENCES tipo_boleta (id_tipo_boleta)
);

CREATE TABLE IF NOT EXISTS viaje_programado
(
  id_viaje_programado serial PRIMARY KEY,
  fecha_salida        date          NOT NULL,
  hora_salida         time          NOT NULL,
  precio_nivel_uno    decimal(8, 2) NOT NULL,
  precio_nivel_dos    decimal(8, 2) NOT NULL,
  asientos_ocupados   int           NOT NULL,
  id_ruta             int           NOT NULL,
  id_bus              int           NOT NULL,
  id_admin_created    int           NOT NULL,
  id_chofer           int           NOT NULL,
  CONSTRAINT viaje_programado_chofer_id_chofer_fk
    FOREIGN KEY (id_chofer) REFERENCES chofer (id_chofer),
  CONSTRAINT viaje_programado_ruta_id_ruta_fk
    FOREIGN KEY (id_ruta) REFERENCES ruta (id_ruta)
);

CREATE TABLE IF NOT EXISTS pasaje
(
  id_pasaje           serial PRIMARY KEY,
  fecha_compra        timestamp     NOT NULL,
  precio_neto         decimal(8, 2) NOT NULL,
  igv                 decimal(8, 2) NOT NULL,
  precio_total        decimal(8, 2) NOT NULL,
  id_pasajero         int           NULL,
  id_asiento          int           NOT NULL,
  id_viaje_programado int           NOT NULL,
  id_transaccion      int           NOT NULL,
  fecha_modificacion  timestamp     NULL,
  id_admin_mod        int           NULL,
  CONSTRAINT pasaje_admin_id_admin_fk
    FOREIGN KEY (id_admin_mod) REFERENCES admin (id_admin),
  CONSTRAINT pasaje_asiento_id_asiento_fk
    FOREIGN KEY (id_asiento) REFERENCES asiento (id_asiento),
  CONSTRAINT pasaje_pasajero_id_pasajero_fk
    FOREIGN KEY (id_pasajero) REFERENCES pasajero (id_pasajero),
  CONSTRAINT pasaje_transaccion_id_transaccion_fk
    FOREIGN KEY (id_transaccion) REFERENCES transaccion (id_transaccion),
  CONSTRAINT pasaje_viaje_programado_id_viaje_programado_fk
    FOREIGN KEY (id_viaje_programado) REFERENCES viaje_programado (id_viaje_programado)
);
