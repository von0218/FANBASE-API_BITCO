import os
import traceback
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import engine, get_db, SessionLocal

# Initialize Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Adventure Time Fanbase API")
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
                models.Character(name="Finn the Human", species="Human", actor_id=actors["jeremy"].id),
                models.Character(name="Jake the Dog", species="Magical Dog", actor_id=actors["john"].id),
                models.Character(name="Princess Bubblegum", species="Gum Person", actor_id=actors["hynden"].id),
                models.Character(name="Marceline the Vampire Queen", species="Vampire/Demon", actor_id=actors["olivia"].id),
                models.Character(name="Ice King", species="Wizard", actor_id=actors["tom"].id),
                models.Character(name="BMO", species="Console", actor_id=actors["niki"].id),
                models.Character(name="Lumpy Space Princess", species="Lumpy Space Person", actor_id=actors["pendleton"].id),
                models.Character(name="Flame Princess", species="Fire Elemental", actor_id=actors["jessica"].id),
                models.Character(name="Lady Rainicorn", species="Rainicorn", actor_id=actors["niki"].id),
                models.Character(name="Gunther", species="Penguin", actor_id=actors["tom"].id)
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
    try:
        characters = db.query(models.Character).all()
        return templates.TemplateResponse(
            request=request, 
            name="index.html", 
            context={"characters": characters}
        )
    except Exception:
        return HTMLResponse(content=f"<pre>{traceback.format_exc()}</pre>", status_code=500)

@app.get("/characters")
def get_all_characters(db: Session = Depends(get_db)):
    return db.query(models.Character).all()

@app.get("/actors")
def get_actors(db: Session = Depends(get_db)):
    return db.query(models.Actor).all()
