from fastapi import FastAPI
from app.routers import auth

app = FastAPI()

app.include_router(auth.router)

@app.get('/')
async def health_check():
    return {'message': 'Medha AI running'}