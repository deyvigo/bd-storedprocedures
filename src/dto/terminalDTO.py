from pydantic import BaseModel, constr


class TerminalDTO(BaseModel):
  id_terminal: int 
  nombre: constr(min_length=1, max_length=255)
  departamento: constr(min_length=1, max_length=100)
  provincia: constr(min_length=1, max_length=100)
