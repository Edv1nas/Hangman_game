from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship

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
    is_active = Column(Boolean, default=True)

    game_stats = relationship("GameStats", back_populates="account")
