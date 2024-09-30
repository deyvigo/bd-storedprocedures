import pymysql
import pymysql.cursors
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

class Connection:
  def __init__(self) -> None:
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute('SHOW TABLES')
      tables = cursor.fetchall()
      if tables.__len__() > 0:
        print('Base de datos ya está creada')
      else:
        self.create_database()
        print('Base de datos creada')
    except Exception as e:
      print(f'Error durante la creación de la base de datos: {e}')

  def create_database(self):
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute('begin;')

      cursor.execute('''
        create table if not exists admin
        (
          id_admin         int auto_increment
            primary key,
          username         varchar(50)  not null,
          password         varchar(80)  not null,
          nombres          varchar(255) not null,
          apellido_pat     varchar(50)  not null,
          apellido_mat     varchar(50)  not null,
          fecha_nacimiento date         not null,
          dni              varchar(10)  not null,
          sexo             varchar(20)  not null,
          telefono         varchar(20)  not null,
          correo           varchar(255) null
        );
      ''')

      cursor.execute('''
        create table if not exists cliente
        (
          id_cliente       int auto_increment
            primary key,
          username         varchar(50)  not null,
          password         varchar(80)  not null,
          dni              varchar(10)  not null,
          nombres          varchar(255) not null,
          apellido_pat     varchar(50)  not null,
          apellido_mat     varchar(50)  null,
          fecha_nacimiento date         not null,
          sexo             varchar(20)  not null,
          telefono         varchar(20)  not null,
          correo           varchar(255) not null
        );
      ''')

      cursor.execute('''
        create table if not exists descuento
        (
          id_descuento int auto_increment
            primary key,
          codigo       varchar(30)   not null,
          monto        decimal(4, 2) not null,
          estado       varchar(20)   not null,
          id_admin     int           not null,
          constraint descuento_admin_id_admin_fk
            foreign key (id_admin) references admin (id_admin)
        );
      ''')

      cursor.execute('''
        create table if not exists metodo_pago
        (
          id_metodo_pago    int auto_increment
            primary key,
          metodo            varchar(20) not null,
          numero_tarjeta    varchar(16) not null,
          fecha_vencimiento varchar(10) not null,
          cvv               varchar(5)  not null,
          id_cliente        int         not null,
          constraint metodo_pago_cliente_id_cliente_fk
            foreign key (id_cliente) references cliente (id_cliente)
        );
      ''')

      cursor.execute('''
        create table if not exists pasajero
        (
          id_pasajero      int auto_increment
            primary key,
          dni              varchar(10)  not null,
          nombres          varchar(255) null,
          apellido_pat     varchar(50)  null,
          apellido_mat     varchar(50)  not null,
          fecha_nacimiento date         not null,
          sexo             varchar(20)  not null
        );
      ''')

      cursor.execute('''
        create table if not exists terminal
        (
          id_terminal int auto_increment
            primary key,
          nombre      varchar(255) not null,
          latitud     double       null,
          longitud    double       null
        );
      ''')

      cursor.execute('''
        create table if not exists tipo_boleta
        (
          id_tipo_boleta int auto_increment
            primary key,
          tipo           varchar(20) not null
        );
      ''')

      cursor.execute('''
        create table if not exists tipo_servicio
        (
          id_tipo_servicio int auto_increment
            primary key,
          servicio         varchar(20) not null
        );
      ''')

      cursor.execute('''
        create table if not exists bus
        (
          id_bus           int auto_increment
            primary key,
          asientos         int         not null,
          placa            varchar(7)  not null,
          marca            varchar(40) not null,
          niveles          int         not null,
          id_tipo_servicio int         not null,
          constraint bus_tipo_servicio_id_tipo_servicio_fk
            foreign key (id_tipo_servicio) references tipo_servicio (id_tipo_servicio)
        );
      ''')

      cursor.execute('''
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
      ''')

      cursor.execute('''
        create table if not exists transaccion
        (
          id_transaccion    int auto_increment
            primary key,
          precio_neto       decimal(10, 2) not null,
          igv               decimal(10, 2) not null,
          percio_total      decimal(10, 2) not null,
          fecha_compra      datetime       not null,
          ruc               varchar(20)    null,
          correo_contacto   varchar(255)   null,
          telefono_contacto varchar(20)    null,
          id_cliente        int            not null,
          id_descuento      int            null,
          id_tipo_boleta    int            not null,
          constraint transaccion_cliente_id_cliente_fk
            foreign key (id_cliente) references cliente (id_cliente),
          constraint transaccion_descuento_id_descuento_fk
            foreign key (id_descuento) references descuento (id_descuento),
          constraint transaccion_tipo_boleta_id_tipo_boleta_fk
            foreign key (id_tipo_boleta) references tipo_boleta (id_tipo_boleta)
        );
      ''')

      cursor.execute('''
        create table if not exists viaje
        (
          id_viaje          int auto_increment
            primary key,
          duracion_estimada time        null,
          distancia         double      null,
          estado            varchar(20) null,
          id_origen         int         not null,
          id_destino        int         not null,
          constraint viaje_terminal_id_terminal_fk
            foreign key (id_origen) references terminal (id_terminal),
          constraint viaje_terminal_id_terminal_fk_2
            foreign key (id_destino) references terminal (id_terminal)
        );
      ''')

      cursor.execute('''
        create table if not exists viaje_programado
        (
          id_viaje_programado int auto_increment
            primary key,
          fecha_salida        date           not null,
          hora_salida         time           not null,
          precio_nivel_uno    decimal(10, 2) not null,
          precio_nivel_dos    decimal(10, 2) null,
          asientos_ocupados   int default 0  not null,
          id_viaje            int            not null,
          id_bus              int            not null,
          id_admin_created    int            not null,
          constraint viaje_programado_admin_id_admin_fk
            foreign key (id_admin_created) references admin (id_admin),
          constraint viaje_programado_bus_id_bus_fk
            foreign key (id_bus) references bus (id_bus),
          constraint viaje_programado_viaje_id_viaje_fk
            foreign key (id_viaje) references viaje (id_viaje)
        );
      ''')

      cursor.execute('''
        create table if not exists pasaje
        (
          id_pasaje           int auto_increment
            primary key,
          fecha_compra        datetime       not null,
          precio_neto         decimal(10, 2) not null,
          igv                 decimal(10, 2) not null,
          precio_total        decimal(10, 2) not null,
          id_pasajero         int            not null,
          id_asiento          int            not null,
          id_viaje_programado int            not null,
          id_transaccion      int            not null,
          fecha_modificacion  datetime       null,
          id_admin_mod        int            null,
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
      ''')

      db.commit()
    except Exception as e:
      print(f'Error durante la creación de la base de datos: {e}')
      db.rollback()

  def connection(self):
    db = pymysql.connections.Connection(
      host=os.getenv('DB_HOST'),
      user=os.getenv('DB_USER'),
      password=os.getenv('DB_PASSWORD'),
      database=os.getenv('DB_NAME'),
      port=int(os.getenv('DB_PORT')),
      cursorclass= pymysql.cursors.DictCursor,
      autocommit=False
    )
    return db