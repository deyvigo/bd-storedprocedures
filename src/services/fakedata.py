from faker import Faker
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
  sexo = fake.random_element(['masculino', 'femenino'])
  args = [nombre, apellido_pat, apellido_mat, sexo, 0, 0, '']
  with db.cursor() as cursor:
    cursor.callproc("sp_register_chofer", args)

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
n_pasajeros = 300

for _ in range(n_pasajeros):
  dni = fake.ean(length=8)
  nombre = fake.first_name()
  apellido_pat = fake.last_name()
  apellido_mat = fake.last_name()
  fecha_nacimiento = fake.date_between(start_date='-70y', end_date='-10y')
  sexo = fake.random_element(['masculino', 'femenino'])
  args = [dni, nombre, apellido_pat, apellido_mat, fecha_nacimiento, sexo, 0, 0, '']
  with db.cursor() as cursor:
    cursor.callproc("sp_register_pasajero", args)