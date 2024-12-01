import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

class Database:
  def __init__(self) -> None:
    db = self.connection()
    try:
      cursor = db.cursor()
      cursor.execute('SHOW TABLES;')
      tables = cursor.fetchall()
      if tables.__len__() > 0:
        print('Conexión: Base de datos ya está creada')
      else:
        self.create_database()
        print('Conexión: Base de datos creada')
    except Exception as e:
      print(f'Error durante la creación de la base de datos: {e}')

  def create_database(self):
    db = self.connection()
    try:
      with db.cursor() as cursor:
        cursor.execute('begin;')
        path = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sql')
        with open(path, 'r') as file:
          sql = file.read()
          cursor.execute(sql)
        db.commit()
        print('Base de datos creada')
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
      autocommit=False,
      client_flag=CLIENT.MULTI_STATEMENTS
    )
    return db

  def load_all_procedures(self):
    db = self.connection()
    try:
      with db.cursor() as cursor:
        cursor.execute('begin;')
        dir_procedures_path = os.path.join(os.path.dirname(__file__), '..', 'procedures')
        sql_files = [f for f in os.listdir(dir_procedures_path) if f.endswith('.sql')]
        for f_sql in sql_files:
          with open(os.path.join(dir_procedures_path, f_sql), 'r') as file:
            sql = file.read()
            if sql:
              try:
                cursor.execute(sql)
              except Exception as e:
                print(f'Error en el procedimiento {f_sql}: {e}')
        db.commit()
        print('Procedimientos cargados')
    except Exception as e:
      print(f'Error durante la creación de los procedimientos: {e}')
      db.rollback()
    finally:
      db.close()

  def delete_all_procedures(self):
    db = self.connection()
    try:
      with db.cursor() as cursor:
        sql = """
          SELECT ROUTINE_NAME
          FROM information_schema.ROUTINES
          WHERE ROUTINE_TYPE = 'PROCEDURE' AND ROUTINE_SCHEMA = %s;
        """
        db_name = os.getenv('DB_NAME')
        cursor.execute(sql, (db_name,))
        procs = cursor.fetchall()
        if procs.__len__() > 0:
          for proc in procs:
            cursor.execute(f"DROP PROCEDURE {proc['ROUTINE_NAME']};")
          db.commit()
          print('Procedimientos eliminados')
        else:
          print('No hay procedimientos para eliminar')
    except Exception as e:
      print(f'Error durante la eliminación de los procedimientos: {e}')

  def create_triggers(self):
    db = self.connection()
    try:
      with db.cursor() as cursor:
        dir_triggers_path = os.path.join(os.path.dirname(__file__), '..', 'triggers')
        sql_files = [f for f in os.listdir(dir_triggers_path) if f.endswith('.sql')]
        for f_sql in sql_files:
          with open(os.path.join(dir_triggers_path, f_sql), 'r') as file:
            sql = file.read()
            if sql:
              try:
                cursor.execute(sql)
              except Exception as e:
                print(f'Error en el procedimiento {f_sql}: {e}')
        db.commit()
        print('Triggers creados')
    except Exception as e:
      print(f'Error durante la creación de los triggers: {e}')
      db.rollback()
    finally:
      db.close()
      
      
  def delete_all_triggers(self):
    db = self.connection()
    try:
      with db.cursor() as cursor:
        sql = """
          SELECT TRIGGER_NAME
          FROM information_schema.TRIGGERS
          WHERE TRIGGER_SCHEMA = %s;
        """
        db_name = os.getenv('DB_NAME')
        cursor.execute(sql, (db_name,))
        procs = cursor.fetchall()
        if procs.__len__() > 0:
          for proc in procs:
            cursor.execute(f"DROP TRIGGER {proc['TRIGGER_NAME']};")
          db.commit()
          print('Triggers eliminados')
        else:
          print('No hay triggers para eliminar')
    except Exception as e:
      print(f'Error durante la eliminación de los triggers: {e}') 
