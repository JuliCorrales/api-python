from werkzeug.exceptions import HTTPException
from fastapi import HTTPException
import jwt
import datetime

from adapter.odoo_adapter import OdooAdapter

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"



def create_jwt_token(data: dict):
    data.update({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira en 1 hora
    })

    token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return token

class AuthService:

    odoo_adapter = OdooAdapter()

    @staticmethod
    def register(client):
        try:
            name = client.name
            dni = client.dni
            email = client.password
            username = client.username
            password = client.password
            client = odoo_adapter.instance.execute(
                'proyect_sales.client_auth',
                'login',
                name,
                dni,
                email,
                username,
                password,
            )
            return client

        except HTTPException as httpe:
            raise httpe
        except Exception as e:
            raise e

    @staticmethod
    def login(login_form: dict):
        try:
            username = login_form.get('username')
            password = login_form.get('password')
            client_data = OdooAdapter.instance.execute(
                'proyect_sales.client_auth',
                'login',
                username,
                password,
            )
            if client_data:
                token = create_jwt_token(client_data)
                return {'token': token, 'type': 'bearer'}
            else:
                raise HTTPException(status_code=400, detail="Nombre de usuario o contraseña incorrectos")

        except HTTPException as httpe:
            raise httpe
        except Exception as e:
            raise e
