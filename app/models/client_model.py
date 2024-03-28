from pydantic import BaseModel

class Client(BaseModel):
    name: str
    dni: int
    email: str
    username: str
    password: str
