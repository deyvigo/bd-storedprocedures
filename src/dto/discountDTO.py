from pydantic import BaseModel, constr, confloat

class DiscountDTO(BaseModel):
  codigo: constr(min_length=1, max_length=30)
  monto: confloat(ge=0.0, le=999.99)
  estado: constr(min_length=1, max_length=20)
