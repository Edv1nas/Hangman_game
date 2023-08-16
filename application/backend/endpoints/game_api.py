from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from random_word import RandomWords

from hangman import HangmanGame
import crud.account_crud
from database.db import get_db
from schemas.game_schemas import GameCreate
from schemas.guess_schemas import GuessInput

from crud.game_crud import create_game, get_game, update_game_status
from crud.letter_crud import create_letter, get_letters_for_game
from schemas.game_schemas import GameCreate
from schemas.letter_schemas import LetterCreate

router = APIRouter()

random_words = RandomWords()
active_games = {}


@router.post("/accounts/{account_id}/games/")
def start_new_game(account_id: int, db: Session = Depends(get_db)):

    random_word = random_words.get_random_word()
    active_game = HangmanGame(random_word)
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
    db_game = get_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    guessed_letter = letter.letter.lower()

    active_game = active_games.get(game_id)
    if active_game is None:
        raise HTTPException(
            status_code=404, detail="Active game not found")

    already_guessed = guessed_letter in active_game.guessed_letters

    if already_guessed:
        return {"message": "You already guessed this letter. Try again."}

    guessed_correctly = active_game.guess_letter(guessed_letter)

    if guessed_correctly:
        game_status = "in_progress"
        if active_game.check_win():
            game_status = "won"
            active_games.pop(game_id)
            # update_game_status(db, game_id, game_status)
    else:
        active_game.count_made_attempts()

        game_status = "in_progress"
        if active_game.check_loss():
            game_status = "lost"
            active_games.pop(game_id)
            # update_game_status(db, game_id, game_status)

    update_game_status(db, game_id, game_status,
                       made_tries=active_game.attempts)

    masked_word = active_game.display_word()
    remaining_attempts = active_game.count_left_attempts()

    create_letter(db, letter, game_id)

    return {
        "game_status": game_status,
        "masked_word": masked_word,
        "remaining_attempts": remaining_attempts
    }


@router.post("/games/{game_id}/resume/")
def resume_game(game_id: int, db: Session = Depends(get_db)):
    db_game = get_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    guessed_letters = get_letters_for_game(db, game_id)

    active_game = HangmanGame(db_game.word)
    active_game.letters = list(db_game.word)
    active_game.guessed_letters = set(
        [letter.letter for letter in guessed_letters])

    if db_game.game_status == "in_progress":
        active_games[game_id] = active_game
        return active_game
    else:
        raise HTTPException(
            status_code=400, detail="Cannot resume game, it's not in progress")
