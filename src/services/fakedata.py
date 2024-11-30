from faker import Faker
import psycopg2
from psycopg2.extras import DictCursor
from flask_bcrypt import Bcrypt
from .database import Database

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
        db.commit()  # Commit after each procedure call
