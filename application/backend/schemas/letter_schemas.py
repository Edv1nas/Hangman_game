from pydantic import BaseModel


class LetterBase(BaseModel):
    letter: str


class LetterCreate(LetterBase):
    pass


class Letter(LetterBase):
    letter_id: int
    game_id: int
    input_time: str

    class Config:
        orm_mode = True
