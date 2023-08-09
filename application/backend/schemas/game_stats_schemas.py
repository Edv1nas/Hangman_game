from datetime import datetime
from pydantic import BaseModel


class GameStatsResponse(BaseModel):
    id: int
    creation_date: datetime
    status: str
    made_tries: int
    score: int
