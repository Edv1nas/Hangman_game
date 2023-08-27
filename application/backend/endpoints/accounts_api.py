from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from crud.game_crud import calculate_win_loss_counts
import crud.account_crud
from crud.account_crud import create_account, get_account
from database.db import get_db
from schemas.account_schemas import AccountCreate, AccountResponse


router = APIRouter()


@router.post("/accounts/", response_model=AccountCreate)
def create_new_account(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, account)


@router.get("/accounts/{account_id}", response_model=AccountResponse)
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
