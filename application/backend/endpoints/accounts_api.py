import logging.config
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud.account_crud as account_crud
from database.db import get_db
from schemas.account_schemas import AccountCreate, AccountResponse

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sLogger")


router = APIRouter()



@router.post("/accounts/", response_model=AccountCreate)
def create_new_account(account: AccountCreate, db: Session = Depends(get_db)):
    try:
        return account_crud.create_account(db, account)
    except Exception as error:
        logger.error("Failed to create new account.", error)
        raise HTTPException(status_code=500, detail="Failed to create new account.")


@router.get("/accounts/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = account_crud.get_account(db, account_id)
    if db_account is None:
        logger.error("Account not found")
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.get("/by_email/{email}", response_model=AccountResponse)
def get_account_by_email(email: str, db: Session = Depends(get_db)):
    account = account_crud.get_account_by_email(db, email=email)
    if not account:
        logger.error("Account not found")
        raise HTTPException(status_code=404, detail="Account not found")
    return account