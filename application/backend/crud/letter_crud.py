import logging.config
from sqlalchemy.orm import Session
from models.letters import Letters
from typing import List, Set

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


def create_letter(db: Session, letter: str, game_id: int) -> Letters:
    try:
        db_letter = Letters(letter=letter, game_id=game_id)
        db.add(db_letter)
        db.commit()
        db.refresh(db_letter)
        return db_letter
    except Exception as e:
        db.rollback()
        logger.error("Error occurred while creating a letter.", e)
        return None

def get_letters_by_game_id(db: Session, game_id: int) -> List[Letters]:
    try:
        return db.query(Letters).filter(Letters.game_id == game_id).all()
    except Exception as e:
        logger.error("Error occurred while fetching letters by game id.", e)
        return []

def get_guessed_letters(db: Session, game_id: int) -> Set[str]:
    try:
        guessed_letters = db.query(Letters).filter(Letters.game_id == game_id).all()
        return {letter.letter for letter in guessed_letters}
    except Exception as e:
        db.rollback()
        logger.error("Error occurred while fetching guessed letters.", e)
        return []
