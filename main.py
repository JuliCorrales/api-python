from fastapi import FastAPI
import uvicorn
from app.routes.login import router as login_router
from app.routes.register import router as register_router
from os import environ

app = FastAPI()

app.include_router(login_router)  # Agrega las rutas de login al enrutador principal
app.include_router(register_router)  # Agrega las rutas de register al enrutador principal

@app.get("/")
def root():
    return environ.get('ROOT_MSG')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(environ.get('PORT')), reload=True)



