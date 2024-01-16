from fastapi import FastAPI
from auth.routers import router as auth_router

app = FastAPI(
    title='parserhub'
)

@app.get('/')
def hello():
    return 'Hello Word!!!'

app.include_router(auth_router)

