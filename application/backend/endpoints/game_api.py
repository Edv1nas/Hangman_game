from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from utils.hangman_game import Hangman
from crud.account_crud import get_account, get_account_stats
from crud.game_crud import get_games_history
from database.db import get_db
from schemas.game_schemas import GameCreate, GameResponse, GameHistoryResponse
from schemas.account_schemas import AccountStats


router = APIRouter()


@router.post("/create/{account_id}", response_model=GameCreate)
def create_game(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    hangman_game = Hangman()
    return hangman_game.create_game(db, db_account.id)


@router.post("/play/{game_id}", response_model=GameResponse)
def play_hang_game(game_id: int, letter: str, db: Session = Depends(get_db)):
    hangman_game = Hangman()
    return hangman_game.play_game(db, game_id, letter)


@router.get("/game-history/{account_id}", response_model=list[GameHistoryResponse])
def get_player_game_history(account_id: int, db: Session = Depends(get_db)):
    games_history = get_games_history(db, account_id)
    if not games_history:
        raise HTTPException(status_code=404, detail="Game history not found")
    return games_history


@router.get("/account/{account_id}/stats", response_model=AccountStats)
def get_player_stats(account_id: int, db: Session = Depends(get_db)):
    stats = get_account_stats(db, account_id)
    if stats is None:
        return {"message": "Account not found"}
    return stats
