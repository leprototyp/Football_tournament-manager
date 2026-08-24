from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    """Liste tous les matchs"""
    matches = db.query(models.Match).all()
    return [
        {
            "match_id": m.match_id,
            "match_date": str(m.match_date),
            "home_score": m.home_score,
            "away_score": m.away_score,
            "tournament_id": m.tournament_id,
            "home_team_id": m.home_team_id,
            "away_team_id": m.away_team_id
        }
        for m in matches
    ]
