from fastapi import APIRouter
from app.service.auth_service import AuthService
from app.models.models import Client

router = APIRouter()

# Ruta para el inicio de sesión y generación de token JWT
@router.post("/api/register")
async def register(client: Client):
    response = AuthService.register(client)
    return {
            'response_data': response
        }