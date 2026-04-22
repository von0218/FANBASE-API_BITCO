import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Explicitly import from local files
import models
from database import engine, get_db, SessionLocal

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Adventure Time Fanbase API",
    description="An API for the Land of Ooo - Characters and Voice Actors"
)

# Seeding logic to ensure the DB isn't empty on Render
@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        # Check if any actors exist; if not, seed the database
        if not db.query(models.Actor).first():
            print("Seeding database with Adventure Time data...")
            
            # Define all Actors
            actors_list = {
                "jeremy": models.Actor(name="Jeremy Shada"),
                "john": models.Actor(name="John DiMaggio"),
                "hynden": models.Actor(name="Hynden Walch"),
                "olivia": models.Actor(name="Olivia Olson"),
                "tom": models.Actor(name="Tom Kenny"),
                "niki": models.Actor(name="Niki Yang"),
                "pendleton": models.Actor(name="Pendleton Ward"),
                "jessica": models.Actor(name="Jessica DiCicco")
            }
            db.add_all(actors_list.values())
            db.commit()

            # Define all Characters
            characters = [
                models.Character(name="Finn the Human", species="Human", actor_id=actors_list["jeremy"].id),
                models.Character(name="Jake the Dog", species="Magical Dog", actor_id=actors_list["john"].id),
                models.Character(name="Princess Bubblegum", species="Gum Person", actor_id=actors_list["hynden"].id),
                models.Character(name="Marceline the Vampire Queen", species="Vampire/Demon", actor_id=actors_list["olivia"].id),
                models.Character(name="Ice King", species="Wizard", actor_id=actors_list["tom"].id),
                models.Character(name="BMO", species="Video Game Console", actor_id=actors_list["niki"].id),
                models.Character(name="Lumpy Space Princess", species="Lumpy Space Person", actor_id=actors_list["pendleton"].id),
                models.Character(name="Flame Princess", species="Fire Elemental", actor_id=actors_list["jessica"].id),
                models.Character(name="Lady Rainicorn", species="Rainicorn", actor_id=actors_list["niki"].id),
                models.Character(name="Gunther", species="Penguin", actor_id=actors_list["tom"].id)
            ]
            db.add_all(characters)
            db.commit()
            print("Seeding complete!")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

# --- Endpoints ---

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Adventure Time API",
        "instructions": "Go to /docs to see the interactive API documentation."
    }

@app.get("/characters")
def get_all_characters(db: Session = Depends(get_db)):
    # Joining with Actor table to get the name directly
    return db.query(models.Character).all()

@app.get("/characters/{char_id}")
def get_character(char_id: int, db: Session = Depends(get_db)):
    char = db.query(models.Character).filter(models.Character.id == char_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found in Ooo")
    
    return {
        "id": char.id,
        "name": char.name,
        "species": char.species,
        "voice_actor": char.voice_actor.name if char.voice_actor else "Unknown"
    }

@app.get("/actors")
def get_actors(db: Session = Depends(get_db)):
    return db.query(models.Actor).all()
