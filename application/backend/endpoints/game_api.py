from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from utils.hangman_game import Hangman
from crud.account_crud import get_account, get_account_stats
from crud.game_crud import get_games_history, get_game
from database.db import get_db
from schemas.game_schemas import GameCreate, GameResponse, GameHistoryResponse
from schemas.account_schemas import AccountStats
from schemas.letter_schemas import LetterResponse
import string


router = APIRouter()

class StringInsteadOfLetterError(HTTPException):
     def __init__(self, value):
        detail = f"Invalid input: String '{value}' received instead of a letter."
        super().__init__(status_code=403, detail=detail)


@router.post("/create/{account_id}", response_model=GameCreate)
def create_game(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    hangman_game = Hangman()
    return hangman_game.create_game(db, db_account.id)


@router.post("/play/{game_id}", response_model=GameResponse)
def play_hang_game(game_id: int, letter: LetterResponse, db: Session = Depends(get_db)):
    hangman_game = Hangman()
    # casted_letter = str(letter)
    # print(casted_letter)
    # print(len(casted_letter))
    # if len(casted_letter) != 10 or letter not in string.ascii_lowercase:
    #     raise StringInsteadOfLetterError(letter)
    return hangman_game.play_game(db, game_id, letter.letter)


@router.get("/game_history/{account_id}", response_model=list[GameHistoryResponse])
def get_player_game_history(account_id: int, db: Session = Depends(get_db)):
    games = get_games_history(db, account_id)
    if not games:
        raise HTTPException(status_code=404, detail="Game history not found")
    return games


@router.get("/account/{account_id}/stats", response_model=AccountStats)
def get_player_stats(account_id: int, db: Session = Depends(get_db)):
    stats = get_account_stats(db, account_id)
    if stats is None:
        return {"message": "Account not found"}
    return stats


@router.get("/games/{game_id}/")
def get_game_data(game_id: int, db: Session = Depends(get_db)):
    game_data = get_game(db, game_id)
    if game_data is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return game_data
