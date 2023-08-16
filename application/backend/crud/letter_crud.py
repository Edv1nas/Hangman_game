from sqlalchemy.orm import Session
from schemas.letter_schemas import LetterCreate
from models.letters import Letters


def create_letter(db: Session, letter: LetterCreate, game_id: int):
    db_letter = Letters(**letter.dict(), game_id=game_id)
    db.add(db_letter)
    db.commit()
    db.refresh(db_letter)
    return db_letter


def get_letters_for_game(db: Session, game_id: int):
    return db.query(Letters).filter(Letters.game_id == game_id).all()
