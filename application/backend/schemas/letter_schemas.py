from pydantic import BaseModel


# class LetterInput(BaseModel):
#     letter: str


# class LetterBase(BaseModel):
#     letter: str


class LetterCreate(BaseModel):
    letter: str


# class Letter(LetterBase):
#     letter_id: int
#     game_id: int
#     input_time: str

#     class Config:
#         orm_mode = True
