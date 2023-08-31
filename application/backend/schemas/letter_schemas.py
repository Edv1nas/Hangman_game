from pydantic import BaseModel


class LetterResponse(BaseModel):
    letter: str
