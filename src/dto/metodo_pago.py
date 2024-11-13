from pydantic import BaseModel, Field

class MetodoPagoCreateDTO(BaseModel):
  nombre: str = Field(..., min_length=5, max_length=50)
  numero_tarjeta: str = Field(..., min_length=16, max_length=16)

class MetodoPagoUpdateDTO(BaseModel):
  nombre: str = Field(..., min_length=5, max_length=50)
  numero_tarjeta: str = Field(..., min_length=16, max_length=16)