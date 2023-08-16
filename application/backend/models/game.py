from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, TIMESTAMP, CHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class Game(Base):
    __tablename__ = "game_stats"
    game_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    game_date = Column(TIMESTAMP, default=datetime.now())
    game_status = Column(Enum('in_progress', 'won', 'lost'), nullable=False)
    made_tries = Column(Integer, nullable=False)
    word = Column(String(255), nullable=False)

    account = relationship("Account", back_populates="game")
    letters = relationship("Letters", back_populates="game")
