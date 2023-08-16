from sqlalchemy.orm import Session
from schemas.game_schemas import GameCreate
from models.game import Game


def create_game(db: Session, game: GameCreate, account_id: int):
    db_game = Game(**game.dict(), account_id=account_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_game(db: Session, game_id: int):
    return db.query(Game).filter(Game.game_id == game_id).first()


def update_game_status(db: Session, game_id: int, status: str, made_tries: int):
    db_game = db.query(Game).filter(Game.game_id == game_id).first()
    if db_game:
        db_game.game_status = status
        db_game.made_tries = made_tries
        db.commit()
        db.refresh(db_game)
        return db_game
    return None
