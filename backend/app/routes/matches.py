from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class MatchSchedule(BaseModel):
    tournament_id: int
    home_team_id: int
    away_team_id: int
    match_date: str
    referee: str

@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).all()
    res = []
    for m in matches:
        referee = getattr(m, "referee", "N/A")
        res.append({
            "match_id": m.match_id,
            "match_date": str(m.match_date),
            "referee": referee,
            "tournament_id": m.tournament_id,
            "home_team_id": m.home_team_id,
            "away_team_id": m.away_team_id
        })
    return res

@router.post("/")
def create_match(data: MatchSchedule, db: Session = Depends(get_db)):
    try:
        m_date = datetime.strptime(data.match_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD expected)")

    match_kwargs = {
        "tournament_id": data.tournament_id,
        "home_team_id": data.home_team_id,
        "away_team_id": data.away_team_id,
        "match_date": m_date
    }
    
    if hasattr(models.Match, "referee"):
        match_kwargs["referee"] = data.referee

    new_m = models.Match(**match_kwargs)
    db.add(new_m)
    db.commit()
    db.refresh(new_m)
    return {"message": "Match scheduled", "match_id": new_m.match_id}
