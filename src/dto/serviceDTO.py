from pydantic import BaseModel, constr


class ServiceDTO(BaseModel):
  servicio: constr(min_length=1, max_length=50)
