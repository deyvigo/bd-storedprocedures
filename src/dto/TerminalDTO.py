from pydantic import BaseModel, constr, confloat
class TerminalCreateDTO(BaseModel): 
  nombre: constr(min_length=4, max_length=255)
  departamento: constr(min_length=3, max_length=100)
  provincia: constr(min_length=3, max_length=100)
  