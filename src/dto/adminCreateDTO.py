from pydantic import BaseModel, constr , conint , condecimal ,confloat  
from typing import Literal
from datetime import time

class TerminalCreateDTO(BaseModel): 
  nombre: constr(min_length=4, max_length=255)
  departamento: constr(min_length=3, max_length=100)
  provincia: constr(min_length=3, max_length=100)

class BusCreateDTO(BaseModel):
  asientos: int
  placa: constr(min_length=6, max_length=7)
  marca: constr(min_length=3, max_length=50)
  niveles: Literal[1,2]
  id_tipo_servicio_bus: Literal[1,2]

class AsientoDTO(BaseModel):
  id_bus: int
  nivel:Literal[1,2]
  numero:conint(ge=1,le=40)

class RutaDTO(BaseModel):
    duracion_estimada: time
    distancia: condecimal(gt=0)  
    id_origen: conint(gt=0)  
    id_destino: conint(gt=0)  
    estado:constr(min_length=1, max_length=50)

class ParadaDTO(BaseModel):
  ordinal:int
  id_terminal: int
  id_ruta: int