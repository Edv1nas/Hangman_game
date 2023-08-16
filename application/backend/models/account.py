from sqlalchemy import Boolean, Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

from database.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    total_games_played = Column(Integer)
    total_wins = Column(Integer)
    total_losses = Column(Integer)
    win_rate = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.now())
    is_active = Column(Boolean, default=True)

    game = relationship("Game", back_populates="account")
