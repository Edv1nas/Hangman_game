from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from crud.game_crud import calculate_win_loss_counts
import crud.account_crud
from crud.account_crud import create_account, get_account
from database.db import get_db
from schemas.account_schemas import AccountCreate, AccountResponse


router = APIRouter()


@router.post("/accounts/")
def create_new_account(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, account)


@router.get("/accounts/{account_id}")
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.get("/by_email/{email}", response_model=AccountResponse)
def get_account_by_email(email: str, db: Session = Depends(get_db)):
    account = crud.account_crud.get_account_by_email(
        db, email=email)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.get("", response_model=list[AccountResponse])
def read_accounts(db: Session = Depends(get_db)):
    accounts = crud.account_crud.get_accounts(db)
    return accounts


@router.post("/update_account_stats/{account_id}")
def update_account_stats(account_id: int, db: Session = Depends(get_db)):
    total_games, total_wins, total_losses = calculate_win_loss_counts(
        db, account_id)
    win_rate = total_wins / total_games * 100 if total_games > 0 else 0
    win_rate_formated = "{:.2f}".format(win_rate)

    updated_account = crud.account_crud.update_account(
        db, account_id, total_games, total_wins, total_losses, win_rate_formated)

    if updated_account:
        return updated_account
    else:
        raise HTTPException(status_code=404, detail="Account not found")
