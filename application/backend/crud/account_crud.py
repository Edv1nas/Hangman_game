# pylint: disable= missing-docstring
import logging.config
from sqlalchemy.orm import Session
from schemas.account_schemas import AccountCreate
from models.account import Account
from typing import Optional, Dict, Union


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


def create_account(db: Session, account: AccountCreate) -> Account:
    try:
        db_account = Account(**account.dict())
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        db.rollback()
        logger.error("Error occurred while creating an account.", e)
        return None

def get_account(db: Session, account_id: int) -> Optional[Account]:
    try:
        return db.query(Account).filter(Account.id == account_id).first()
    except Exception as e:
        logger.error("Error occurred while fetching an account.", e)
        return None

def get_account_by_email(db: Session, email: str) -> Optional[Account]:
    try:
        return db.query(Account).filter(Account.email == email).first()
    except Exception as e:
        logger.error("Error occurred while fetching an account by email.", e)
        return None

def update_account_stats(db: Session, account_id: int, game_status: str) -> None:
    try:
        account = db.query(Account).filter(Account.id == account_id).first()

        if account:
            account.total_games_played += 1
            if game_status == "Victory":
                account.total_wins += 1
            elif game_status == "Defeat":
                account.total_losses += 1

            if account.total_games_played > 0:
                account.win_rate = (account.total_wins / account.total_games_played) * 100
            else:
                account.win_rate = 0.0

            db.commit()
    except Exception as e:
        db.rollback()
        logger.error("Error occurred while updating account stats.", e)
        return None

def get_account_stats(db: Session, account_id: int) -> Optional[Dict[str, Union[int, float]]]:
    try:
        account = db.query(Account).filter(Account.id == account_id).first()

        if account:
            return {
                "total_games_played": account.total_games_played,
                "total_wins": account.total_wins,
                "total_losses": account.total_losses,
                "win_rate": account.win_rate,
            }
        return None
    except Exception as e:
        logger.error("Error occurred while fetching account stats.", e)
        return None