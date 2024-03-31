from xmlrpc import client
from os import environ
from fastapi import HTTPException, status
import logging

ODOO_URL = environ.get('ODOO_URL')
ODOO_DB = environ.get('ODOO_DB')
ODOO_USER = environ.get('ODOO_USER')
ODOO_PASSWD = environ.get('ODOO_PASSWD')


class OdooAdapter:
    instance = None

    uid: int
    common = client.ServerProxy('{}/xmlrpc/2/common'.format(ODOO_URL), allow_none=True)
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
            pass
        if not self.uid:
            pass

    def execute(self, model, method, *args, **kwargs):
        if not self.uid:
            self.login()

        if not self.uid:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='No se puede conectar con el '
                                                                                        'servidor de Odoo. ('
                                                                                        'uid %s)' % self.uid)

        try:
            return self.models.execute_kw(
                ODOO_DB, self.uid, ODOO_PASSWD,
                model, method,
                list(args), kwargs
            )

        except client.Fault as cf:
            logging.error(str(cf))
            # raise cf
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f'{cf.faultString} ({cf.faultCode})')

        except Exception as ex:
            logging.error(str(ex))
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Error al ejecutar el método '
                                                                                        '%s contra el servidor de '
                                                                                        'Odoo -> %s' % (method,
                                                                                                        str(ex)))
