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


@router.post("/")
def create_tournament(tournament: dict, db: Session = Depends(get_db)):
    """Création sécurisée d'un tournoi"""
    from datetime import datetime
    
    start = tournament.get("start_date")
    end = tournament.get("end_date")
    
    if isinstance(start, str):
        start = datetime.strptime(start, "%Y-%m-%d").date()
    if isinstance(end, str):
        end = datetime.strptime(end, "%Y-%m-%d").date()

    new_t = models.Tournament(
        name=tournament.get("name"),
        start_date=start,
        end_date=end,
        organizer_id=tournament.get("organizer_id", 1)
    )
    db.add(new_t)
    db.commit()
    db.refresh(new_t)
    return {
        "tournament_id": new_t.tournament_id,
        "name": new_t.name,
        "start_date": str(new_t.start_date),
        "end_date": str(new_t.end_date)
    }


@router.delete("/{tournament_id}", status_code=204)
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    t = db.query(models.Tournament).filter(models.Tournament.tournament_id == tournament_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tournament not found")
    db.query(models.Match).filter(models.Match.tournament_id == tournament_id).delete()
    db.delete(t)
    db.commit()
    return None
