from fastapi import APIRouter
from app.service.auth_service import AuthService

router = APIRouter()

# Ruta para el inicio de sesión y generación de token JWT
@router.post("/api/auth")
async def login(login_form: dict):
    return await AuthService.login(login_form)