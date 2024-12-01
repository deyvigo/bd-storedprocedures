from datetime import date
from pydantic import BaseModel, constr


class PasajeroDTO(BaseModel):
  dni: constr(min_length=8, max_length=8)
  nombre: constr(min_length=1, max_length=255)
  apellido_pat: constr(min_length=1, max_length=50)
  apellido_mat: constr(min_length=1, max_length=50)
  fecha_nacimiento: date
  sexo: constr(min_length=1, max_length=15)
