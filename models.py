from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationship to link actors to the characters they voice
    characters = relationship("Character", back_populates="voice_actor")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    
    # This column is required for the new wiki-accurate abilities
    ability = Column(String, nullable=True)
    
    # Foreign key to the Actor table
    actor_id = Column(Integer, ForeignKey("actors.id"))

    # Relationship to access actor details from a character object
    voice_actor = relationship("Actor", back_populates="characters")
