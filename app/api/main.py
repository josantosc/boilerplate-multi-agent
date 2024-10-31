from fastapi import APIRouter

from app.api.routes import login, users, whatsapp, use_case

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(whatsapp.router, prefix="/whebhook", tags=["whebhook"])
api_router.include_router(use_case.router, prefix="/use_case", tags=["use_case"])



