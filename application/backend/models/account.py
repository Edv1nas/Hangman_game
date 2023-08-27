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
    total_games_played = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP, default=datetime.now())
    is_active = Column(Boolean, default=True)

    game = relationship("Game", back_populates="account")
