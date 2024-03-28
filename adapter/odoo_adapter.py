from xmlrpc import client
from werkzeug.exceptions import HTTPException
from os import environ
import logging

ODOO_URL = environ.get('ODOO_URL')
ODOO_DB = environ.get('ODOO_DB')
ODOO_USER = environ.get('ODOO_USER')
ODOO_PASSWD = environ.get('ODOO_PASSWD')


class OdooAdapter:

    instance = None

    uid: int
    common = client.ServerProxy('{}/xmlrpc/2/common'.format(ODOO_URL))
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(ODOO_URL), allow_none=True)

    def __init__(self, user='', passwd='', global_instance=True):
        if global_instance:
            OdooAdapter.instance = self

        self.user = user or ODOO_USER
        self.passwd = passwd or ODOO_PASSWD

        self.login()

    def login(self):
        self.uid = 0

        try:
            self.uid = OdooAdapter.common.authenticate(
                ODOO_DB,
                self.user,
                self.passwd,
                {}
            )
        except Exception as e:
            logging.error(str(e))

        if not self.uid:
            logging.error('Error al iniciar sesión en Odoo')

    def execute(self, model, method, *args, **kwargs):
        if not self.uid:
            logging.warning('No se inició sesión en Odoo CRM, reintentando')
            self.login()

        if not self.uid:
            return {
                'status': 504,
                'error': f'No se puede conectar con el servidor de Odoo ({self.uid})',
            }

        try:
            return self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWD,
                model, method,
                list(args), kwargs
            )
        except client.Fault as cf:
            logging.error(str(cf))
            raise cf
        except TypeError as te:
            logging.error(str(te))
            raise HTTPException(description=str(te))
        except Exception as e:
            logging.error(str(e))
            odoo_exception = self.is_odoo_exception(e)
            if odoo_exception:
                return {
                    'status': 418, #or 409, 423,
                    'error': odoo_exception
                }
            return {
                'status': 504,
                'error': 'No se puede conectar con el servidor de Odoo',
            }
    def is_odoo_exception(self, error):
        try:
            faultStr = error.faultString.split(f"\n")

            for line in faultStr:
                if 'odoo.exceptions' in line:
                    return line
            return False
        except:
            return False