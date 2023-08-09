from database.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class GameStats(Base):
    __tablename__ = "game_stats"
    id = Column(Integer, primary_key=True, index=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)
    made_tries = Column(Integer)
    score = Column(Integer)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="game_stats")
