from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from pydantic import BaseModel

router = APIRouter()

class TeamCreate(BaseModel):
    name: str
    coach_name: str

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    res = []
    for t in teams:
        coach = getattr(t, "coach_name", None) or getattr(t, "coach", "N/A")
        res.append({
            "team_id": t.team_id,
            "name": t.name,
            "coach_name": coach
        })
    return res

@router.post("/")
def create_team(data: TeamCreate, db: Session = Depends(get_db)):
    try:
        # Tente de créer avec 'coach_name', sinon tente avec 'coach'
        if hasattr(models.Team, "coach_name"):
            new_team = models.Team(name=data.name, coach_name=data.coach_name)
        elif hasattr(models.Team, "coach"):
            new_team = models.Team(name=data.name, coach=data.coach_name)
        else:
            new_team = models.Team(name=data.name)
            
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return {"message": "Team created", "team_id": new_team.team_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    t = db.query(models.Team).filter(models.Team.team_id == team_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Supprime ou détache les matchs impliquant cette équipe pour éviter les erreurs de contrainte
    db.query(models.Match).filter(
        (models.Match.home_team_id == team_id) | (models.Match.away_team_id == team_id)
    ).delete(synchronize_session=False)
    
    db.delete(t)
    db.commit()
    return None
