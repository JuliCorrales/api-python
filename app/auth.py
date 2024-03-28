# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from passlib.context import CryptContext
# import jwt
# from datetime import datetime, timedelta

# SECRET_KEY = "super-secret"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# # Configuración de seguridad
# pwd_context = CryptContext(schemes=["bcrypt"])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Función para el registro de usuarios
# async def register_user(username: str, password: str, db: Database = Depends(database)):
#     hashed_password = get_password_hash(password)
#     query = "INSERT INTO users (username, password) VALUES (:username, :password)"
#     values = {"username": username, "password": hashed_password}
#     await db.execute(query=query, values=values)
