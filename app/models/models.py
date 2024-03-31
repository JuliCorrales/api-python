from pydantic import BaseModel

class Client(BaseModel):
    name: str
    dni: int
    email: str
    username: str
    password: str

class LoginForm(BaseModel):
    username: str
    password: str