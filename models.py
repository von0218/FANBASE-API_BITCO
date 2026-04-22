from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    characters = relationship("Character", back_populates="voice_actor")

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    ability = Column(String, nullable=True) # Added for wiki abilities
    actor_id = Column(Integer, ForeignKey("actors.id"))
    voice_actor = relationship("Actor", back_populates="characters")
