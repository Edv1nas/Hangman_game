from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    games = relationship("GameInfo", back_populates="player")
