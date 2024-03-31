from fastapi import APIRouter
from app.service.auth_service import AuthService
from app.models.models import LoginForm

router = APIRouter()

# Ruta para el inicio de sesión y generación de token JWT
@router.post("/api/auth")
async def login(login_form: LoginForm):
    response = AuthService.login(login_form)
    return {
        'response_data': response
    }