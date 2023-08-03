from base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class GameInfo(Base):
    __tablename__ = "game_info"
    id = Column(Integer, primary_key=True, index=True)
    game_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)
    tries = Column(Integer)
    word = Column(String)
    score = Column(Integer)

    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="games")
