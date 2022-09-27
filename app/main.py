from fastapi import FastAPI

from .routers.users import users

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")


@app.get('/health')
def health():
    return True
