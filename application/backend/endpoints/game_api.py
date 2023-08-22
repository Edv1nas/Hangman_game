from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from hangman_game import HangmanGame
import crud.account_crud
from database.db import get_db
from schemas.game_schemas import GameCreate
from schemas.guess_schemas import GuessInput

from crud.game_crud import create_game, get_game, update_game_status, get_word_by_game_id
from crud.letter_crud import create_letter, get_letters_for_game, get_letters_by_game_id
from schemas.game_schemas import GameCreate
from schemas.letter_schemas import LetterCreate
from game_checks import (
    validate_game_exists,
    validate_active_game,
    validate_letter_not_guessed)

router = APIRouter()

active_games = {}

@router.get("/games/{game_id}")
def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    validate_game_exists(db, game_id)
    db_game = get_game(db, game_id)
    return db_game


@router.post("/accounts/{account_id}/games/")
def start_new_game(account_id: int, db: Session = Depends(get_db)):

    active_game = HangmanGame()
    random_word = active_game.get_word()
    active_game.split_word()

    game_data = {
        "word": random_word,
        "game_status": "in_progress",
        "made_tries": 0
    }
    game = create_game(db, GameCreate(**game_data), account_id)

    active_games[game.game_id] = active_game

    return game


@router.post("/games/{game_id}/letters/")
def make_guess(
    game_id: int,
    letter: LetterCreate,
    db: Session = Depends(get_db)
):
    validate_game_exists(db, game_id)

    guessed_letter = letter.letter.lower()

    active_game = active_games.get(game_id)

    validate_active_game(active_games, game_id)

    validate_letter_not_guessed(active_game, guessed_letter)

    guessed_correctly = active_game.guess_letter(guessed_letter)

    if guessed_correctly:
        game_status = "in_progress"
        if active_game.check_win():
            game_status = "Victory"
            active_games.pop(game_id)
    else:
        active_game.count_made_attempts()

        game_status = "in_progress"
        if active_game.check_loss():
            game_status = "Defeat"
            active_games.pop(game_id)

    update_game_status(db, game_id, game_status,
                       made_tries=active_game.attempts)

    masked_word = active_game.display_word()
    remaining_attempts = active_game.count_left_attempts()
    active_game.guessed_letters.add(guessed_letter)
    guessed_letters = ', '.join(active_game.guessed_letters)    
    create_letter(db, letter, game_id)

    return {
        "game_status": game_status,
        "masked_word": masked_word,
        "remaining_attempts": remaining_attempts,
        "guessed_letters": guessed_letters
    }
