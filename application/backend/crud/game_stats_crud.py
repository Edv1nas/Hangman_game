from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from models.game_stats import GameStats


def get_game_stats(db: Session, game_stats_id: int):
    return db.query(GameStats).filter(GameStats.id == game_stats_id).first()


def get_game_stats_by_account(db: Session, account_id: int):
    return db.query(GameStats).filter(GameStats.account_id == account_id).all()


def delete_game_stats(db: Session, game_stats_id: int):
    db_game_stats = db.query(GameStats).filter(
        GameStats.id == game_stats_id).first()
    if db_game_stats:
        db.delete(db_game_stats)
        db.commit()
    return db_game_stats
