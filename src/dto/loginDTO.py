from pydantic import BaseModel, constr

class AdminLoginDTO(BaseModel):
  username: constr(min_length=3, max_length=50)
  password: constr(min_length=8, max_length=80)

class ClientLoginDTO(BaseModel):
  username: constr(min_length=3, max_length=50)
  password: constr(min_length=8, max_length=80)