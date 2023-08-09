from fastapi import APIRouter

from endpoints import accounts_api, game_stats_api

api_router = APIRouter()

api_router.include_router(accounts_api.router,
                          prefix="/accounts",
                          tags=["accounts"])

api_router.include_router(game_stats_api.router,
                          prefix="/game_stats",
                          tags=["game_stats"])
