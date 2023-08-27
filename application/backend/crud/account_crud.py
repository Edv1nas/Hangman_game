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


def update_account_stats(db: Session, account_id: int, game_status: str):
    account = db.query(Account).filter(Account.id == account_id).first()

    if account:
        account.total_games_played += 1
        if game_status == "Victory":
            account.total_wins += 1
        elif game_status == "Defeat":
            account.total_losses += 1

        if account.total_games_played > 0:
            account.win_rate = (account.total_wins /
                                account.total_games_played) * 100
        else:
            account.win_rate = 0.0
        db.add(account)
        db.commit()


def get_account_stats(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()

    if account:
        return {
            "total_games_played": account.total_games_played,
            "total_wins": account.total_wins,
            "total_losses": account.total_losses,
            "win_rate": account.win_rate,
        }
    return None
