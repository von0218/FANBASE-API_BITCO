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
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        # Check if the database is missing characters
        if not db.query(models.Character).first():
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

            # The Full Character List based on GitHub files
            characters = [
                models.Character(name="Finn the Human", species="Human", actor_id=actors["jeremy"].id, ability="Heroism & Master Swordsmanship"),
                models.Character(name="Jake the Dog", species="Magical Dog", actor_id=actors["john"].id, ability="Elastic Stretchy Powers"),
                models.Character(name="Princess Bubblegum", species="Gum Person", actor_id=actors["hynden"].id, ability="Scientific Genius & Alchemy"),
                models.Character(name="Marceline", species="Vampire", actor_id=actors["olivia"].id, ability="Soul Sucking & Shapeshifting"),
                models.Character(name="Ice King", species="Wizard", actor_id=actors["tom"].id, ability="Snow & Ice Manipulation"),
                models.Character(name="BMO", species="Console", actor_id=actors["niki"].id, ability="Digital Reality & Video Games"),
                models.Character(name="Lumpy Space Princess", species="Lumpy Space Person", actor_id=actors["pendleton"].id, ability="Lumpy Bite & Floating"),
                models.Character(name="Flame Princess", species="Fire Elemental", actor_id=actors["jessica"].id, ability="Pyrokinesis & Heat Generation"),
                models.Character(name="Lady Rainicorn", species="Rainicorn", actor_id=actors["niki"].id, ability="Chromatic Flight & Phasing"),
                models.Character(name="Gunther", species="Penguin", actor_id=actors["tom"].id, ability="Cosmic Slap & Hidden Eldritch Power")
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
