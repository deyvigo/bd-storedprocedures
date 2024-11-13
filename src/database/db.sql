create table if not exists admin
(
  id_admin         int auto_increment
    primary key,
  nombre           varchar(255) not null,
  apellido_pat     varchar(50)  not null,
  apellido_mat     varchar(50)  not null,
  fecha_nacimiento date         not null,
  dni              varchar(8)   not null,
  sexo             varchar(15)  not null,
  telefono         varchar(20)  not null,
  correo           varchar(255) not null,
  username         varchar(50)  not null,
  password         varchar(80)  not null
);

create table if not exists chofer
(
  id_chofer    int auto_increment
    primary key,
  nombre       varchar(255) not null,
  apellido_pat varchar(50)  not null,
  apellido_mat varchar(50)  not null,
  dni          varchar(8)   not null,
  sexo         varchar(15)  not null
);

create table if not exists cliente
(
  id_cliente       int auto_increment
    primary key,
  dni              varchar(8)   not null,
  nombre           varchar(255) not null,
  apellido_pat     varchar(50)  not null,
  apellido_mat     varchar(50)  not null,
  fecha_nacimiento date         not null,
  sexo             varchar(15)  not null,
  telefono         varchar(20)  not null,
  correo           varchar(100) not null,
  username         varchar(50)  not null,
  password         varchar(80)  not null
);

create table if not exists descuento
(
  id_descuento int auto_increment
    primary key,
  codigo       varchar(30)   not null,
  monto        decimal(8, 2) not null,
  estado       varchar(20)   not null,
  id_admin     int           not null,
  constraint descuento_admin_id_admin_fk
    foreign key (id_admin) references admin (id_admin)
);

create table if not exists metodo_pago
(
  id_metodo_pago    int auto_increment
    primary key,
  nombre            varchar(50) not null,
  numero_tarjeta    varchar(16) not null,
  estado            varchar(20) not null default 'activo',
  id_cliente        int         not null
);

create table if not exists pasajero
(
  id_pasajero      int auto_increment
    primary key,
  dni              varchar(8)   not null,
  nombre           varchar(255) not null,
  apellido_pat     varchar(50)  not null,
  apellido_mat     varchar(50)  not null,
  fecha_nacimiento date         not null,
  sexo             varchar(15)  not null
);

create table if not exists terminal
(
  id_terminal  int auto_increment
    primary key,
  nombre       varchar(255) not null,
  departamento varchar(100) not null,
  provincia    varchar(100) not null
);

create table if not exists parada_intermedia
(
  id_parada_intermedia int auto_increment
    primary key,
  ordinal              int not null,
  id_terminal          int not null,
  id_ruta              int not null,
  constraint parada_intermedia_terminal_id_terminal_fk
    foreign key (id_terminal) references terminal (id_terminal)
);

create table if not exists ruta
(
  id_ruta           int auto_increment
    primary key,
  duracion_estimada time        not null,
  distancia         double      not null,
  estado            varchar(20) not null,
  id_origen         int         not null,
  id_destino        int         not null,
  constraint ruta_terminal_id_terminal_fk
    foreign key (id_origen) references terminal (id_terminal),
  constraint ruta_terminal_id_terminal_fk_2
    foreign key (id_destino) references terminal (id_terminal)
);

create table if not exists tipo_boleta
(
  id_tipo_boleta int auto_increment
    primary key,
  tipo           varchar(20) not null
);

create table if not exists tipo_servicio_bus
(
  id_tipo_servicio_bus int auto_increment
    primary key,
  servicio             varchar(50) not null
);

create table if not exists bus
(
  id_bus               int auto_increment
    primary key,
  asientos             int         not null,
  placa                varchar(7)  not null,
  marca                varchar(50) not null,
  niveles              int         not null,
  id_tipo_servicio_bus int         not null,
  constraint bus_tipo_servicio_bus_id_tipo_servicio_bus_fk
    foreign key (id_tipo_servicio_bus) references tipo_servicio_bus (id_tipo_servicio_bus)
);

create table if not exists asiento
(
  id_asiento int auto_increment
    primary key,
  nivel      int not null,
  numero     int not null,
  id_bus     int not null,
  constraint asiento_bus_id_bus_fk
    foreign key (id_bus) references bus (id_bus)
);

create table if not exists transaccion
(
  id_transaccion    int auto_increment
    primary key,
  precio_neto       decimal(8, 2) not null,
  igv               decimal(8, 2) not null,
  precio_total      decimal(8, 2) not null,
  fecha_compra      datetime      not null,
  ruc               varchar(20)   null,
  correo_contacto   varchar(255)  not null,
  telefono_contacto varchar(20)   not null,
  id_cliente        int           not null,
  id_descuento      int               null,
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
  id_viaje_programado int auto_increment
    primary key,
  fecha_salida        date          not null,
  hora_salida         time          not null,
  precio_nivel_uno    decimal(8, 2) not null,
  precio_nivel_dos    decimal(8, 2) not null,
  asientos_ocupados   int           not null,
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
  id_pasaje           int auto_increment
    primary key,
  fecha_compra        datetime      not null,
  precio_neto         decimal(8, 2) not null,
  igv                 decimal(8, 2) not null,
  precio_total        decimal(8, 2) not null,
  id_pasajero         int           null,
  id_asiento          int           not null,
  id_viaje_programado int           not null,
  id_transaccion      int           not null,
  fecha_modificacion  datetime      null,
  id_admin_mod        int           null,
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
