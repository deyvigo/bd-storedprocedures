from pydantic import BaseModel, constr, Field, EmailStr
from datetime import date

class ClienteDTO(BaseModel):
  id_cliente: int
  nombre: constr(min_length=1, max_length=255)
  apellido_pat: constr(min_length=1, max_length=50)
  apellido_mat: constr(min_length=1, max_length=50)
  fecha_nacimiento: date
  dni: constr(min_length=8, max_length=8) = Field(..., pattern=r'^\d{8}$')
  sexo: constr(min_length=1, max_length=15)
  telefono: constr(min_length=9, max_length=20) = Field(..., pattern=r'^\+?\d{9,20}$')
  correo: EmailStr
  username: constr(min_length=3, max_length=50)
  password: constr(min_length=8, max_length=80)