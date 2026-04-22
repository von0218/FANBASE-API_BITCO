import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
from database import engine, get_db, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Adventure Time Fanbase API")

# Mount templates - Ensure your folder is named 'templates' in GitHub
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if not db.query(models.Actor).first():
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
    except Exception as e:
        print(f"Seed Error: {e}")
    finally:
        db.close()

@app.get("/")
def read_root():
    return RedirectResponse(url="/ui")

@app.get("/ui", response_class=HTMLResponse)
def get_ui(request: Request, db: Session = Depends(get_db)):
    try:
        characters = db.query(models.Character).all()
        return templates.TemplateResponse("index.html", {"request": request, "characters": characters})
    except Exception as e:
        # This will show you the error in the browser if the page fails
        return HTMLResponse(content=f"<html><body><h1>UI Error</h1><p>{str(e)}</p></body></html>", status_code=500)

@app.get("/characters")
def get_all_characters(db: Session = Depends(get_db)):
    return db.query(models.Character).all()

@app.get("/actors")
def get_actors(db: Session = Depends(get_db)):
    return db.query(models.Actor).all()
