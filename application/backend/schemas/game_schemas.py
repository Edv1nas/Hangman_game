from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class GameCreate(BaseModel):
    game_id: int
    game_status: str
    game_date: datetime
    game_word: str
    attempts: int

    class Config:
        orm_model = True
        json_schema_extra = {
            "example": {
                "game_id": "3",
                "game_status": "in_progress",
                "game_date": "2023-08-26 20:43:56.984731",
                "game_word": "keksas",
                "attempts": "1",
            }
        }


class GameResponse(BaseModel):
    masked_word: str
    game_status: str
    entered_letters: List[str]
    attempts: int
    message: str

    class Config:
        orm_model = True
        json_schema_extra = {
            "example": {
                "masked_word": "l _ _ _ _ _",
                "game_status": "in_progress",
                "entered_letters": ["a"],
                "attempts": "1",
                "message": "",
            }
        }


class GameHistoryResponse(BaseModel):
    account_id: int
    game_id: int
    game_status: str
    game_word: str
    game_date: datetime
    attempts: int

    class Config:
        orm_model = True
        json_schema_extra = {
            "example": {
                "account_id": "1",
                "game_id": "1",
                "game_status": "in_progress",
                "game_word": "keksas",
                "game_date": "2023-08-26 20:43:56.984731",
                "attempts": "1",
            }
        }
