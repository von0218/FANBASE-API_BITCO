import os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db, SessionLocal

# Rebuilds tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mounts the root directory for your MP3 and PNGs
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        # If the database is empty, fill it with cards!
        if not db.query(models.Character).first():
            actors = {
                "jeremy": models.Actor(name="Jeremy Shada"),
                "john": models.Actor(name="John DiMaggio"),
                "hynden": models.Actor(name="Hynden Walch"),
                "olivia": models.Actor(name="Olivia Olson")
            }
            db.add_all(actors.values())
            db.commit()

            characters = [
                models.Character(name="Finn the Human", species="Human", actor_id=actors["jeremy"].id, 
                                 ability="Master Swordsman & Heroism: Skilled in multiple martial arts and immune to the Lich's mind control."),
                models.Character(name="Jake the Dog", species="Magical Dog", actor_id=actors["john"].id, 
                                 ability="Stretchy Powers: Can modify the size, shape, and dimensions of every part of his body."),
                models.Character(name="Princess Bubblegum", species="Gum Person", actor_id=actors["hynden"].id, 
                                 ability="Scientific Genius: Master of candy-based technology, alchemy, and biological engineering."),
                models.Character(name="Marceline the Vampire Queen", species="Vampire/Demon", actor_id=actors["olivia"].id, 
                                 ability="Soul Sucking & Shapeshifting: Can absorb souls, turn invisible, and transform into monstrous forms.")
            ]
            db.add_all(characters)
            db.commit()
    finally:
        db.close()

@app.get("/")
def read_root():
    return RedirectResponse(url="/ui")

@app.get("/ui", response_class=HTMLResponse)
async def get_ui(request: Request, db: Session = Depends(get_db)):
    characters = db.query(models.Character).all()
    return templates.TemplateResponse(request=request, name="index.html", context={"characters": characters})
