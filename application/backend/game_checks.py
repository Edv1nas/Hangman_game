from fastapi import HTTPException
from hangman_game import HangmanGame
from crud.game_crud import get_game

def validate_game_exists(db, game_id):
    db_game = get_game(db, game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

def validate_active_game(active_games, game_id):
    active_game = active_games.get(game_id)
    if active_game is None:
        raise HTTPException(status_code=404, detail="Active game not found")

def validate_letter_not_guessed(active_game, guessed_letter):
    already_guessed = guessed_letter in active_game.guessed_letters
    if already_guessed:
        raise HTTPException(status_code=400, detail="Letter already guessed")