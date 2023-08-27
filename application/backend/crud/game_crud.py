from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from models.game import Game
from models.account import Account
from crud.account_crud import update_account_stats


def get_game(db: Session, game_id: int):
    return db.query(Game).filter(Game.game_id == game_id).first()


def get_games_by_user_id(db: Session, user_id: int) -> Account:
    user = db.query(Account).filter(Account.id == user_id).first()
    if user:
        return user.games
    else:
        raise NoResultFound


def update_game_status(db: Session, game_id: int, status: str, attempts: int):
    db_game = db.query(Game).filter(Game.game_id == game_id).first()
    if db_game:
        db_game.game_status = status
        db_game.attempts = attempts
        db.commit()
        db.refresh(db_game)
        return db_game
    return None


def get_games_history(db: Session, account_id: int):
    return db.query(Game).filter(Game.account_id == account_id).all()


def get_word_by_game_id(db: Session, game_id: int):
    return db.query(Game.word).filter(Game.game_id == game_id).first()


def get_account_id_from_game_id(db: Session, game_id: int) -> int:
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if game:
        return game.account_id
    return None


def update_account_stats_from_game(db: Session, game_id: int, is_win: bool):
    game = db.query(Game).filter(Game.game_id == game_id).first()

    if game:
        account_id = game.account_id
        update_account_stats(db, account_id, is_win)
