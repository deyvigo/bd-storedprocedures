from pydantic import BaseModel, EmailStr, constr, Field
from datetime import date

class AdminSignUpDTO(BaseModel):
  nombre: constr(min_length=1, max_length=255)
  apellido_pat: constr(min_length=1, max_length=50)
  apellido_mat: constr(min_length=1, max_length=50)
  fecha_nacimiento: date  # Validación automática de formato de fecha
  dni: constr(min_length=8, max_length=8) = Field(..., pattern=r'^\d{8}$')  # Solo 8 dígitos
  sexo: constr(min_length=1, max_length=15)
  telefono: constr(min_length=9, max_length=20) = Field(..., pattern=r'^\+?\d{9,20}$')  # Puede incluir un '+' y entre 9 y 20 dígitos
  correo: EmailStr  # Valida que sea un correo electrónico válido
  username: constr(min_length=3, max_length=50)
  password: constr(min_length=8, max_length=80)

class ClientSignUpDTO(BaseModel):
  nombre: constr(min_length=1, max_length=255)
  apellido_pat: constr(min_length=1, max_length=50)
  apellido_mat: constr(min_length=1, max_length=50)
  fecha_nacimiento: date  # Validación automática de formato de fecha
  dni: constr(min_length=8, max_length=8) = Field(..., pattern=r'^\d{8}$')  # Solo 8 dígitos
  sexo: constr(min_length=1, max_length=15)
  telefono: constr(min_length=9, max_length=20) = Field(..., pattern=r'^\+?\d{9,20}$')  # Puede incluir un '+' y entre 9 y 20 dígitos
  correo: EmailStr  # Valida que sea un correo electrónico válido
  username: constr(min_length=3, max_length=50)
  password: constr(min_length=8, max_length=80)
