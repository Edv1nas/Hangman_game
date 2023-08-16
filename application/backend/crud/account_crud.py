from sqlalchemy.orm import Session
from schemas.account_schemas import AccountCreate
from models.account import Account


def create_account(db: Session, account: AccountCreate):
    db_account = Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def get_account_by_email(db: Session, email: str):
    return db.query(Account).filter(Account.email == email).first()


def get_accounts(db: Session):
    return db.query(Account).all()


def update_account(db: Session, account_id: int, total_games_played: int, total_wins: int, total_losses: int, win_rate: float):
    db_account = db.query(Account).filter(Account.id == account_id).first()

    if db_account:
        db_account.total_games_played = total_games_played
        db_account.total_wins = total_wins
        db_account.total_losses = total_losses
        db_account.win_rate = win_rate

        db.commit()
        db.refresh(db_account)
        return db_account

    return None
