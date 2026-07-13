"""Barcha handlerlarni bitta routerga yig'ish."""
from aiogram import Router

from . import common, citizen, operator, admin, fallback


def get_main_router() -> Router:
    router = Router()
    router.include_router(common.router)
    router.include_router(citizen.router)
    router.include_router(operator.router)
    router.include_router(admin.router)
    router.include_router(fallback.router)  # catch-all — oxirida
    return router
