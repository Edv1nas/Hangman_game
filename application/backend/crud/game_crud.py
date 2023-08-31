import logging.config
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from models.game import Game
from models.account import Account
from typing import Optional

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


def get_game(db: Session, game_id: int) -> Optional[Game]:
    try:
        return db.query(Game).filter(Game.game_id == game_id).first()
    except Exception as e:
        logger.error("Error occurred while fetching a game.", e)
        return None


def get_games_by_user_id(db: Session, user_id: int) -> Optional[Game]:
    try:
        user = db.query(Account).filter(Account.id == user_id).first()
        if user:
            return user.games
        else:
            raise NoResultFound
    except NoResultFound as e:
        logger.error(f"No games found for user with id {user_id}.", e)
        raise e
    except Exception as e:
        logger.error("Error occurred while fetching games by user id.", e)
        return []

def update_game_status(db: Session, game_id: int, status: str, attempts: int) -> Optional[Game]:
    try:
        db_game = db.query(Game).filter(Game.game_id == game_id).first()
        if db_game:
            db_game.game_status = status
            db_game.attempts = attempts
            db.commit()
            db.refresh(db_game)
            return db_game
        return None
    except Exception as e:
        db.rollback()
        logger.error("Error occurred while updating game status.", e)
        return None

def get_games_history(db: Session, account_id: int) -> Optional[Game]:
    try:
        return db.query(Game).filter(Game.account_id == account_id).all()
    except Exception as e:
        logger.error("Error occurred while fetching game history.", e)
        return []

def get_word_by_game_id(db: Session, game_id: int) -> Optional[str]:
    try:
        return db.query(Game.word).filter(Game.game_id == game_id).first()
    except Exception as e:
        logger.error("Error occurred while fetching word by game id.", e)
        return None

def get_account_id_from_game_id(db: Session, game_id: int) -> Optional[int]:
    try:
        game = db.query(Game).filter(Game.game_id == game_id).first()
        if game:
            return game.account_id
        return None
    except Exception as e:
        logger.error("Error occurred while fetching account id from game id.", e)
        return None
