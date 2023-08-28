from pydantic import BaseModel, EmailStr
from datetime import datetime


class AccountCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "Bob",
                "email": "bob@hotmail.com",
                "password": "hotbob112",
            }
        }


class AccountResponse(BaseModel):
    id: int
    username: str
    email: str
    password: str
    total_games_played: int
    total_wins: int
    total_losses: int
    win_rate: float
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": "1",
                "username": "Bob",
                "email": "bob@hotmail.com",
                "password": "hotbob112",
                "total_games_played": "1",
                "total_wins": "0",
                "total_losses": "1",
                "win_rate": "0.0",
                "created_at": "2023-08-26 20:43:56.984731",
                "is_active": "True",
            }
        }


class AccountStats(BaseModel):
    total_games_played: int
    total_wins: int
    total_losses: int
    win_rate: float

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "total_games_played": "1",
                "total_wins": "0",
                "total_losses": "0",
                "win_rate": "0.0",
            }
        }
