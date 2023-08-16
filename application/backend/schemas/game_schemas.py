# from pydantic import BaseModel


# class GameResponse(BaseModel):
#     account_id: int
#     game_id: int
#     game_date: str
#     game_status: str
#     made_tries: int


# class GameCreate(BaseModel):
#     account_id: int
#     game_id: int
#     game_date: str
#     game_status: str
#     made_tries: int

from pydantic import BaseModel
from typing import List


class GameBase(BaseModel):
    game_status: str
    made_tries: int
    word: str


class GameCreate(GameBase):
    pass


class Game(GameBase):
    game_id: int
    account_id: int
    game_date: str
    letters: List["Letter"]

    class Config:
        orm_mode = True
