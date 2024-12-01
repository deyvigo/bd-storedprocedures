create table if not exists admin
(
  id_admin         serial primary key,
  nombre           varchar(255) not null,
  apellido_pat     varchar(50)  not null,
  apellido_mat     varchar(50)  not null,
  fecha_nacimiento date         not null,
  dni              varchar(8)   not null check (length(dni) = 8),
  sexo             varchar(15)  not null check (sexo in ('masculino', 'femenino')),
  telefono         varchar(9)   not null check (length(telefono) = 9),
  correo           varchar(255) not null unique,
  username         varchar(50)  not null unique,
  password         varchar(80)  not null
);

create table if not exists chofer
(
  id_chofer    serial primary key,
  nombre       varchar(255) not null,
  apellido_pat varchar(50)  not null,
  apellido_mat varchar(50)  not null,
  dni          varchar(8)   not null unique check (length(dni) = 8),
  sexo         varchar(15)  not null check (sexo in ('masculino', 'femenino')),
  estado       varchar(20)  not null check (estado in ('contratado', 'despedido')) default 'contratado'
);

create table if not exists cliente
(
  id_cliente       serial primary key,
  dni              varchar(8)   not null unique check (length(dni) = 8),
  nombre           varchar(255) not null,
  apellido_pat     varchar(50)  not null,
  apellido_mat     varchar(50)  not null,
  fecha_nacimiento date         not null,
  sexo             varchar(15)  not null check (sexo in ('masculino', 'femenino')),
  telefono         varchar(20)  not null check (length(telefono) = 9),
  correo           varchar(100) not null unique,
  username         varchar(50)  not null unique,
  password         varchar(80)  not null
);

create table if not exists descuento
(
  id_descuento serial primary key,
  codigo       varchar(30)   not null unique,
  monto        decimal(8, 2) not null check (monto > 0),
  estado       varchar(20)   not null default 'activo' check (estado in ('activo', 'inactivo')),
  id_admin     int           not null,
  constraint descuento_admin_id_admin_fk
    foreign key (id_admin) references admin (id_admin)
);

create table if not exists metodo_pago
(
  id_metodo_pago    serial primary key,
  nombre            varchar(50) not null,
  numero_tarjeta    varchar(16) not null unique check (length(numero_tarjeta) = 16),
  estado            varchar(20) not null default 'activo' check (estado in ('activo', 'inactivo')),
  id_cliente        int         not null
);

create table if not exists pasajero
(
  id_pasajero      serial primary key,
  dni              varchar(8)   not null unique check (length(dni) = 8),
  nombre           varchar(255) not null,
  apellido_pat     varchar(50)  not null,
  apellido_mat     varchar(50)  not null,
  fecha_nacimiento date         not null,
  sexo             varchar(15)  not null check (sexo in ('masculino', 'femenino'))
);

create table if not exists terminal
(
  id_terminal  serial primary key,
  nombre       varchar(255) not null,
  departamento varchar(100) not null,
  provincia    varchar(100) not null
);

create table if not exists parada_intermedia
(
  id_parada_intermedia serial primary key,
  ordinal              int not null check (ordinal > 0),
  id_terminal          int not null,
  id_ruta              int not null,
  constraint parada_intermedia_terminal_id_terminal_fk
    foreign key (id_terminal) references terminal (id_terminal)
);

create table if not exists ruta
(
  id_ruta           serial primary key,
  duracion_estimada time        not null check (duracion_estimada > '00:00:00'),
  distancia         double      not null check (distancia > 0),
  estado            varchar(20) not null default 'activo' check (estado in ('activo', 'inactivo')),
  id_origen         int         not null,
  id_destino        int         not null,
  constraint ruta_terminal_id_terminal_fk
    foreign key (id_origen) references terminal (id_terminal),
  constraint ruta_terminal_id_terminal_fk_2
    foreign key (id_destino) references terminal (id_terminal)
);

create table if not exists tipo_boleta
(
  id_tipo_boleta serial primary key,
  tipo           varchar(20) not null
);

create table if not exists tipo_servicio_bus
(
  id_tipo_servicio_bus serial primary key,
  servicio             varchar(50) not null
);

create table if not exists bus
(
  id_bus               serial primary key,
  asientos             int         not null check (asientos > 0),
  placa                varchar(7)  not null unique check (length(placa) = 7),
  marca                varchar(50) not null,
  niveles              int         not null check (niveles in (1, 2)),
  id_tipo_servicio_bus int         not null,
  constraint bus_tipo_servicio_bus_id_tipo_servicio_bus_fk
    foreign key (id_tipo_servicio_bus) references tipo_servicio_bus (id_tipo_servicio_bus)
);

create table if not exists asiento
(
  id_asiento serial primary key,
  nivel      int not null check (nivel in (1, 2)),
  numero     int not null check (numero > 0),
  id_bus     int not null,
  constraint asiento_bus_id_bus_fk
    foreign key (id_bus) references bus (id_bus)
);

create table if not exists transaccion
(
  id_transaccion    serial primary key,
  precio_neto       decimal(8, 2) not null check (precio_neto > 0),
  igv               decimal(8, 2) not null check (igv > 0),
  precio_total      decimal(8, 2) not null check (precio_total > 0),
  fecha_compra      timestamp     not null,
  ruc               varchar(11)   check (length(ruc) = 11 or ruc is null),
  correo_contacto   varchar(255)  not null,
  telefono_contacto varchar(20)   not null,
  id_cliente        int           not null,
  id_descuento      int           unique,
  id_tipo_boleta    int           not null,
  id_metodo_pago    int           not null,
  constraint transaccion_cliente_id_cliente_fk
    foreign key (id_cliente) references cliente (id_cliente),
  constraint transaccion_descuento_id_descuento_fk
    foreign key (id_descuento) references descuento (id_descuento),
  constraint transaccion_tipo_boleta_id_tipo_boleta_fk
    foreign key (id_tipo_boleta) references tipo_boleta (id_tipo_boleta),
  constraint transaccion_metodo_pago_id_metodo_pago_fk
    foreign key (id_metodo_pago) references metodo_pago (id_metodo_pago)
);

create table if not exists viaje_programado
(
  id_viaje_programado serial primary key,
  fecha_salida        date          not null,
  hora_salida         time          not null,
  precio_nivel_uno    decimal(8, 2) not null check (precio_nivel_uno > 0),
  precio_nivel_dos    decimal(8, 2) not null check (precio_nivel_dos > 0),
  asientos_ocupados   int           not null check (asientos_ocupados >= 0),
  id_ruta             int           not null,
  id_bus              int           not null,
  id_admin_created    int           not null,
  id_chofer           int           not null,
  constraint viaje_programado_chofer_id_chofer_fk
    foreign key (id_chofer) references chofer (id_chofer),
  constraint viaje_programado_ruta_id_ruta_fk
    foreign key (id_ruta) references ruta (id_ruta)
);

create table if not exists pasaje
(
  id_pasaje           serial primary key,
  fecha_compra        timestamp     not null,
  precio_neto         decimal(8, 2) not null check (precio_neto > 0),
  igv                 decimal(8, 2) not null check (igv > 0),
  precio_total        decimal(8, 2) not null check (precio_total > 0),
  id_pasajero         int           not null,
  id_asiento          int           not null,
  id_viaje_programado int           not null,
  id_transaccion      int           not null,
  fecha_modificacion  timestamp,
  id_admin_mod        int,
  constraint pasaje_admin_id_admin_fk
    foreign key (id_admin_mod) references admin (id_admin),
  constraint pasaje_asiento_id_asiento_fk
    foreign key (id_asiento) references asiento (id_asiento),
  constraint pasaje_pasajero_id_pasajero_fk
    foreign key (id_pasajero) references pasajero (id_pasajero),
  constraint pasaje_transaccion_id_transaccion_fk
    foreign key (id_transaccion) references transaccion (id_transaccion),
  constraint pasaje_viaje_programado_id_viaje_programado_fk
    foreign key (id_viaje_programado) references viaje_programado (id_viaje_programado)
);
