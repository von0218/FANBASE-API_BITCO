import os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import engine, get_db, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# IMPORTANT: Mounts your root folder so /static/exit-song.mp3 works
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if not db.query(models.Actor).first():
            actors = {
                "jeremy": models.Actor(name="Jeremy Shada"),
                "john": models.Actor(name="John DiMaggio"),
                "hynden": models.Actor(name="Hynden Walch"),
                "olivia": models.Actor(name="Olivia Olson"),
                "tom": models.Actor(name="Tom Kenny"),
                "niki": models.Actor(name="Niki Yang"),
                "pendleton": models.Actor(name="Pendleton Ward"),
                "jessica": models.Actor(name="Jessica DiCicco")
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
                                 ability="Soul Sucking & Shapeshifting: Can absorb souls, turn invisible, and transform into monstrous forms."),
                models.Character(name="Ice King", species="Wizard", actor_id=actors["tom"].id, 
                                 ability="Frigid Magic: Can create and manipulate ice/snow, fly with his beard, and use 'Wizard Vision'."),
                models.Character(name="BMO", species="Console", actor_id=actors["niki"].id, 
                                 ability="Digital Reality: Can transport people into video games and functions as a multi-purpose electronic device."),
                models.Character(name="Lumpy Space Princess", species="Lumpy Space Person", actor_id=actors["pendleton"].id, 
                                 ability="Lumpy Bite: Her bite can turn others into Lumpy Space people; immune to the effects of the Anti-Element."),
                models.Character(name="Flame Princess", species="Fire Elemental", actor_id=actors["jessica"].id, 
                                 ability="Pyrokinesis: Can generate massive amounts of fire and heat, and transform into a colossal fire giant."),
                models.Character(name="Lady Rainicorn", species="Rainicorn", actor_id=actors["niki"].id, 
                                 ability="Chromatic Flight: Can fly, pass through walls, and change the color of objects with her horn."),
                models.Character(name="Gunther", species="Penguin", actor_id=actors["tom"].id, 
                                 ability="Cosmic Horror: Actually Orgalorg, an ancient deity capable of planet-level destruction and soul manipulation.")
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
