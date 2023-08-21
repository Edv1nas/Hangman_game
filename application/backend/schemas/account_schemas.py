from pydantic import BaseModel


class AccountBase(BaseModel):
    username: str
    email: str


class AccountCreate(AccountBase):
    password: str


class AccountResponse(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class Account(AccountBase):
    id: int
    total_games_played: int
    total_wins: int
    total_losses: int
    win_rate: float
    created_at: str
    is_active: bool

    class Config:
        orm_mode = True
