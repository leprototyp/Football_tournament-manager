from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return [{"team_id": t.team_id, "name": t.name, "coach": t.coach} for t in teams]
