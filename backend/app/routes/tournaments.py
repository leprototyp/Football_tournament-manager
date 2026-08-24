from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/")
def get_tournaments(db: Session = Depends(get_db)):
    """Liste tous les tournois"""
    tournaments = db.query(models.Tournament).all()
    return [
        {
            "tournament_id": t.tournament_id,
            "name": t.name,
            "start_date": str(t.start_date),
            "end_date": str(t.end_date),
            "organizer_id": t.organizer_id
        }
        for t in tournaments
    ]

@router.get("/{tournament_id}")
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Récupère un tournoi par son ID"""
    t = db.query(models.Tournament).filter(models.Tournament.tournament_id == tournament_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return {
        "tournament_id": t.tournament_id,
        "name": t.name,
        "start_date": str(t.start_date),
        "end_date": str(t.end_date),
        "organizer_id": t.organizer_id
    }
