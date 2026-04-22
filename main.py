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

# Mounts the root directory so /static/exit-song.mp3 is accessible
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if not db.query(models.Character).first():
            # Ensure your database population includes the 'ability' field
            # as seen in your UI screenshot
            actors = {"tom": models.Actor(name="Tom Kenny"), "jeremy": models.Actor(name="Jeremy Shada")}
            db.add_all(actors.values())
            db.commit()
            # ... add other characters here ...
    finally:
        db.close()

@app.get("/")
def read_root():
    return RedirectResponse(url="/ui")

@app.get("/ui", response_class=HTMLResponse)
async def get_ui(request: Request, db: Session = Depends(get_db)):
    characters = db.query(models.Character).all()
    return templates.TemplateResponse(request=request, name="index.html", context={"characters": characters})
