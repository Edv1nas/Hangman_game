from sqlalchemy import Column, Integer, ForeignKey, CHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base


class Letters(Base):
    __tablename__ = 'letters'

    letter_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game_stats.game_id'))
    letter = Column(CHAR(1), nullable=False)
    input_time = Column(TIMESTAMP, default=datetime.now())

    game = relationship("Game", back_populates="letters")
