from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import schemas.account_schemas
from models.account import Account


def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def get_account_by_email(db: Session, email: str):
    return db.query(Account).filter(Account.email == email).first()


def get_accounts(db: Session):
    return db.query(Account).all()


def create_account(db: Session, account: schemas.account_schemas.AccountCreate):
    db_account = Account(username=account.username,
                         email=account.email,
                         password=account.password,
                         )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def delete_account(db: Session, account_id: int):
    account = get_account(db, account_id)
    if account:
        db.delete(account)
        db.commit()
        return account
    else:
        raise NoResultFound


def update_account(db: Session, account_id: int, updated_account: schemas.account_schemas.AccountUpdate):
    account = get_account(db, account_id)
    if not account:
        raise NoResultFound

    for field, value in updated_account.dict(exclude_unset=True).items():
        setattr(account, field, value)
    db.commit()
    db.refresh(account)
    return account
