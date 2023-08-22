from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from schemas.game_schemas import GameCreate
from models.game import Game
from models.account import Account


def create_game(db: Session, game: GameCreate, account_id: int):
    db_game = Game(**game.dict(), account_id=account_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_game(db: Session, game_id: int):
    return db.query(Game).filter(Game.game_id == game_id).first()


def get_games_by_user_id(db: Session, user_id: int) -> Account:
    user = db.query(Account).filter(Account.id == user_id).first()
    if user:
        return user.games
    else:
        raise NoResultFound


def update_game_status(db: Session, game_id: int, status: str, made_tries: int):
    db_game = db.query(Game).filter(Game.game_id == game_id).first()
    if db_game:
        db_game.game_status = status
        db_game.made_tries = made_tries
        db.commit()
        db.refresh(db_game)
        return db_game
    return None


def calculate_win_loss_counts(db: Session, account_id: int):
    total_games = db.query(Game).filter(Game.account_id == account_id).count()
    total_wins = db.query(Game).filter(
        Game.account_id == account_id, Game.game_status == "won").count()
    total_losses = total_games - total_wins

    return total_games, total_wins, total_losses

def get_word_by_game_id(db: Session, game_id: int):
    return db.query(Game.word).filter(Game.game_id == game_id).first()