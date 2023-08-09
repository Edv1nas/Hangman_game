from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    total_games_played: int
    total_wins: int
    total_losses: int
    win_rate: float
    is_active: bool

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "Antis",
                "email": "antantas123@gmail.com",
                "password": "1234",
                "total_games_played": 0,
                "total_wins": 0,
                "total_losses": 0,
                "win_rate": 0,
                "is_active": True
            }
        }


class AccountResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    total_games_played: int
    total_wins: int
    total_losses: int
    win_rate: float
    is_active: bool

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "Antis",
                "email": "antantas123@gmail.com",
                "password": "1234",
                "total_games_played": 0,
                "total_wins": 0,
                "total_losses": 0,
                "win_rate": 0,
                "is_active": True
            }
        }


class AccountUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str
    total_games_played: int
    total_wins: int
    total_losses: int
    win_rate: float
    is_active: bool

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "Antis",
                "email": "antantas123@gmail.com",
                "password": "1234",
                "total_games_played": 0,
                "total_wins": 0,
                "total_losses": 0,
                "win_rate": 0,
                "is_active": True
            }
        }
