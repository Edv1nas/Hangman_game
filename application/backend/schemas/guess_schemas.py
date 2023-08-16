from pydantic import BaseModel


class GuessInput(BaseModel):
    letter: str
