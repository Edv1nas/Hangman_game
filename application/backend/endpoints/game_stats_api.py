from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import crud.game_stats_crud
from database.db import get_db
from schemas.game_stats_schemas import GameStatsResponse


router = APIRouter()


@router.get("/gamestats/{game_stats_id}", response_model=GameStatsResponse)
def get_game_stats(game_stats_id: int, db: Session = Depends(get_db)):
    game_stats = crud.game_stats_crud.get_game_stats(db, game_stats_id)
    if not game_stats:
        raise HTTPException(status_code=404, detail="GameStats not found")
    return game_stats


@router.get("/gamestats/by_account/{account_id}", response_model=list[GameStatsResponse])
def get_game_stats_by_account(account_id: int, db: Session = Depends(get_db)):
    game_stats = crud.game_stats_crud.get_game_stats_by_account(db, account_id)
    return game_stats


@router.delete("/gamestats/{game_stats_id}", response_model=GameStatsResponse)
def delete_game_stats(game_stats_id: int, db: Session = Depends(get_db)):
    game_stats = crud.game_stats_crud.delete_game_stats(db, game_stats_id)
    if not game_stats:
        raise HTTPException(status_code=404, detail="GameStats not found")
    return game_stats
