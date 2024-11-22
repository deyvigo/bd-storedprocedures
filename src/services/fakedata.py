from faker import Faker
from pymysql.cursors import DictCursor
from decimal import Decimal
import string

from flask_bcrypt import Bcrypt 
from .database import Database

bcrypt = Bcrypt()
fake = Faker("es_ES")

db = Database().connection()

# admin
n_admins = 1
for _ in range(n_admins):
  nombre = fake.first_name()
  apellido_pat = fake.last_name()
  apellido_mat = fake.last_name()
  fecha_nacimiento = fake.date_between(start_date='-70y', end_date='-10y')
  dni = fake.ean(length=8)
  sexo = fake.random_element(['masculino', 'femenino'])
  telefono = fake.numerify("9########")
  correo = fake.email()
  username = 'admin'
  password = bcrypt.generate_password_hash('12345678').decode('utf-8')
  args = [nombre, apellido_pat, apellido_mat, fecha_nacimiento, dni, sexo, telefono, correo, username, password, 0, 0, '']
  with db.cursor() as cursor:
    cursor.callproc("sp_register_admin", args)

# buses
n_buses = 10

with db.cursor() as cursor:
  cursor.callproc("sp_register_tipo_servicio_bus", ["premium", 0, 0, ''])
  cursor.callproc("sp_register_tipo_servicio_bus", ["basic", 0, 0, ''])

id_bus = 1
for _ in range(n_buses):
  asientos = fake.random_element([30, 40])
  placa = "".join(fake.random_choices(elements=string.ascii_uppercase + string.digits, length=6))
  marca = fake.random_element(['Mercedes', 'Toyota', 'Volkswagen'])
  niveles = fake.random_element([1, 2])
  id_tipo_servicio_bus = fake.random_element([1, 2])
  args = [asientos, placa, marca, niveles, id_tipo_servicio_bus, 0, 0, '']
  with db.cursor() as cursor:
    cursor.callproc("sp_register_bus", args)

  i = 1
  nivel = 1
  # seats
  for _ in range(asientos):
    numero = i
    if niveles == 2:
      if asientos / niveles < i:
        nivel = 2

    with db.cursor() as cursor:
      cursor.callproc("sp_register_asiento", [nivel, numero, id_bus, 0, 0, ''])

    i += 1
  id_bus += 1

# terminals
with db.cursor() as cursor:
  cursor.callproc("sp_register_terminal", ["Terminal 1", "Lima", "Lima", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 2", "Lima", "Huarochirí", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 3", "Lima", "Barranca", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 4", "Ica", "Ica", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 5", "Ica", "Nazca", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 6", "Ica", "Pisco", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 7", "Cusco", "Cuzco", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 8", "Cusco", "Paucartambo", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 9", "Ancash", "Huaraz", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 10", "Ancash", "Huari", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 11", "Arequipa", "Castilla", 0, 0, ''])
  cursor.callproc("sp_register_terminal", ["Terminal 12", "Arequipa", "Arequipa", 0, 0, ''])

  # routes
  cursor.callproc("sp_register_ruta", ["12:00", 10329, 'activo', 1, 9, 0, 0, '']) # 1: Lima - Huaraz
  cursor.callproc("sp_register_ruta", ["24:00", 10329, 'activo', 1, 7, 0, 0, '']) # 2: Lima - Cusco
  cursor.callproc("sp_register_ruta", ["04:00", 10329, 'activo', 1, 4, 0, 0, '']) # 3: Lima - Ica
  cursor.callproc("sp_register_ruta", ["18:00", 10329, 'activo', 1, 12, 0, 0, ''])  # 4: Lima - Arequipa

  # paradas intermedias Lima - Cusco
  cursor.callproc("sp_register_parada_intermedia", [1, 11, 1, 0, 0, ''])
  cursor.callproc("sp_register_parada_intermedia", [2, 12, 1, 0, 0, ''])

  # paradas intermedias Lima - Ica
  cursor.callproc("sp_register_parada_intermedia", [1, 2, 3, 0, 0, ''])
  cursor.callproc("sp_register_parada_intermedia", [1, 3, 3, 0, 0, ''])


# drivers
n_drivers = 10

for _ in range(n_drivers):
  nombre = fake.first_name()
  apellido_pat = fake.last_name()
  apellido_mat = fake.last_name()
  dni = fake.ean(length=8)
  sexo = fake.random_element(['masculino', 'femenino'])
  estado = fake.random_element(['contratado', 'despedido'])
  args = [nombre, apellido_pat, apellido_mat, dni, sexo, 0, 0, '']
  with db.cursor() as cursor:
    cursor.callproc("sp_add_chofer", args)

# trips: 1-4 per route
for i in range(4):
  id_ruta = i + 1
  trips = fake.random_element([1, 2, 3, 4])
  for _ in range(trips):
    fecha_salida = fake.date_between(start_date='-1d', end_date='+4d')
    hora_salida = fake.random_element(["07:00", "19:00"])
    precio_nivel_uno = 70
    precio_nivel_dos = 60
    asientos_ocupados = 0
    id_bus = fake.random_element([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    id_admin_created = 1
    id_chofer = fake.random_element([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    args = [fecha_salida, hora_salida, precio_nivel_uno, precio_nivel_dos, asientos_ocupados, id_ruta, id_bus, id_admin_created, id_chofer, 0, 0, '']
    with db.cursor() as cursor:
      cursor.callproc("sp_register_viaje_programado", args)

# pasengers
passengers = []
n_pasajeros = 300

for _ in range(n_pasajeros):
  dni = fake.ean(length=8)
  nombre = fake.first_name()
  apellido_pat = fake.last_name()
  apellido_mat = fake.last_name()
  fecha_nacimiento = fake.date_between(start_date='-70y', end_date='-10y')
  sexo = fake.random_element(['masculino', 'femenino'])
  args = [dni, nombre, apellido_pat, apellido_mat, fecha_nacimiento, sexo, 0, 0, '']
  passengers.append(args)

# type of billets
with db.cursor() as cursor:
  cursor.callproc("sp_register_tipo_boleta", ["normal", 0, 0, ''])

# trips, buses and seats to be used in the simulation
trips = {}

with db.cursor(cursor=DictCursor) as cursor:
  cursor.execute("SELECT * FROM viaje_programado")
  trips = cursor.fetchall()

# clients
n_clients = 40
for _ in range(n_clients):
  nombre = fake.first_name()
  apellido_pat = fake.last_name()
  apellido_mat = fake.last_name()
  fecha_nacimiento = fake.date_between(start_date='-70y', end_date='-10y')
  dni = fake.ean(length=8)
  sexo = fake.random_element(['masculino', 'femenino'])
  telefono = fake.numerify("9########")
  correo = fake.email()
  username = f'cliente{_ + 1}'
  password = bcrypt.generate_password_hash('12345678').decode('utf-8')
  args = [nombre, apellido_pat, apellido_mat, fecha_nacimiento, dni, sexo, telefono, correo, username, password, 0, 0, '']
  with db.cursor() as cursor:
    cursor.callproc("sp_register_cliente", args)

# payment methods: 1-2 per client
for i in range(n_clients):
  id_cliente = i + 1
  payment_methods = fake.random_element([1, 2])
  for _ in range(payment_methods):
    nombre = f"Tarjeta {_ + 1}"
    number = fake.numerify("4#####XXXXXX####")
    args = [nombre, number, id_cliente, 0, 0, '']
    with db.cursor() as cursor:
      cursor.callproc("sp_register_metodo_pago", args)

id_transaccion = 1
# transactions: 1-4 per client
for i in range(n_clients):
  id_cliente = i + 1
  transactions = fake.random_element([1, 2, 3, 4])

  for _ in range(transactions):
    # select payment method
    payments = []
    with db.cursor() as cursor:
      cursor.execute(f"SELECT * FROM metodo_pago WHERE id_cliente = {id_cliente}")
      payments = cursor.fetchall()

    payment_selected = fake.random_element(payments)
    id_metodo_pago = payment_selected['id_metodo_pago']

    # create transaction
    fecha_compra = fake.date_between(start_date='-10d', end_date='now')
    ruc = fake.random_number(digits=11, fix_len=True)
    correo_contacto = fake.email()
    telefono_contacto = fake.numerify("9########")
    args = [0, 0, 0, fecha_compra, ruc, correo_contacto, telefono_contacto, id_cliente, None, 1, id_metodo_pago, 0, 0, '']
    with db.cursor() as cursor:
      cursor.callproc("sp_register_transaccion", args)
    
    # details -> pasaje only one passenger
    details = fake.random_element([1, 2, 3, 4])
    for _ in range(details):
      
      # select viaje_programado
      viaje_programado = fake.random_element(trips)
      id_viaje_programado = viaje_programado['id_viaje_programado']

      passenger_args = fake.random_element(passengers)
      # search and create if not exists
      passenger = None
      with db.cursor() as cursor:
        cursor.execute(f"SELECT * FROM pasajero WHERE dni = '{passenger_args[0]}'")
        passenger = cursor.fetchone()
        if not passenger:
          cursor.callproc("sp_register_pasajero", passenger_args)
          cursor.execute(f"SELECT * FROM pasajero WHERE dni = '{passenger_args[0]}'")
          passenger = cursor.fetchone()
      
      id_pasajero = passenger['id_pasajero']
      # get all free seats
      free_seats = []
      with db.cursor() as cursor:
        cursor.execute(f"""
          SELECT a.*
          FROM asiento a
          INNER JOIN viaje_programado vp ON a.id_bus = vp.id_bus
          LEFT JOIN pasaje p ON a.id_asiento = p.id_asiento
          WHERE a.id_bus = {viaje_programado['id_bus']} AND vp.id_viaje_programado = {viaje_programado['id_viaje_programado']} AND p.id_pasaje IS NULL;
        """)
        free_seats = cursor.fetchall()
      if not free_seats:
        print(f'No hay asientos libres para el viaje {viaje_programado["id_viaje_programado"]}')
        continue
      # select a random seat
      seat = fake.random_element(free_seats)
      # check position of the seat
      nivel = seat['nivel']
      precio_total = 0
      if nivel == 1:
        precio_total = viaje_programado['precio_nivel_uno']
      elif nivel == 2:
        precio_total = viaje_programado['precio_nivel_dos']
      
      igv = precio_total * Decimal('0.18')
      precio_neto = precio_total - igv

      detail_args = [fecha_compra, precio_neto, igv, precio_total, id_pasajero, seat['id_asiento'], id_viaje_programado, id_transaccion, None, None, 0, 0, '']
      with db.cursor() as cursor:
        cursor.callproc("sp_register_pasaje", detail_args)
        # update transaction prices
        cursor.execute(f"""
          UPDATE transaccion 
          SET precio_neto = precio_neto + {precio_neto},
              precio_total = precio_total + {precio_total},
              igv = igv + {igv}
          WHERE id_transaccion = {id_transaccion};
        """)
        # update seats occupation with trigger
        cursor.execute(f"""
          UPDATE viaje_programado
          SET asientos_ocupados = asientos_ocupados + 1
          WHERE id_viaje_programado = {id_viaje_programado};
        """)

    id_transaccion += 1




print("Base de datos rellenada con datos de ejemplo")

