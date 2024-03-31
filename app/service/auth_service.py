from werkzeug.exceptions import HTTPException
from fastapi import HTTPException, status
import jwt
import datetime
from os import environ
from adapter.odoo_adapter import OdooAdapter

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"

ODOO_USER = environ.get('ODOO_USER')
ODOO_PASSWD = environ.get('ODOO_PASSWD')

def create_jwt_token(data: dict):
    data.update({
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expira en 1 hora
    })
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return token

class AuthService:

    adapter = OdooAdapter(user=ODOO_USER, passwd=ODOO_PASSWD, global_instance=True)

    @staticmethod
    def register(client):
        try:
            response_client = OdooAdapter.instance.execute(
                'proyect_sales.client_auth',
                'register',
                client.dict()
            )
            if response_client:
                return response_client
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='No se puedo crear correctamente el registro del cliente.')

        except HTTPException as httpe:
            raise httpe
        except Exception as e:
            raise e

    @staticmethod
    def login(login_form):
        try:
            client_data = OdooAdapter.instance.execute(
                'proyect_sales.client_auth',
                'login',
                login_form.dict()
            )
            if client_data.get('status_code') == 200:
                token = create_jwt_token(client_data.get('data'))
                return {"status_code": 200, 'token': token, 'type': 'bearer'}
            else:
                raise HTTPException(status_code=400, detail="Nombre de usuario o contraseña incorrectos")

        except HTTPException as httpe:
            raise httpe
        except Exception as e:
            raise e
