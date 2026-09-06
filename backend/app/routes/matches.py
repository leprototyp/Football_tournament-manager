from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class MatchSchedule(BaseModel):
    tournament_id: int
    home_team_id: int
    away_team_id: int
    match_date: str
    referee: str

class MatchScore(BaseModel):
    home_score: int
    away_score: int

def ensure_columns_exist(db: Session):
    for col_def in ["referee VARCHAR", "home_score INTEGER", "away_score INTEGER"]:
        col_name = col_def.split()[0]
        try:
            db.execute(text(f"ALTER TABLE matches ADD COLUMN {col_def};"))
            db.commit()
        except Exception:
            db.rollback()

@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    ensure_columns_exist(db)
    try:
        sql = text("SELECT match_id, match_date, referee, tournament_id, home_team_id, away_team_id, home_score, away_score FROM matches")
        rows = db.execute(sql).fetchall()
        return [
            {
                "match_id": r[0],
                "match_date": str(r[1]),
                "referee": r[2] if r[2] else "N/A",
                "tournament_id": r[3],
                "home_team_id": r[4],
                "away_team_id": r[5],
                "home_score": r[6],
                "away_score": r[7]
            }
            for r in rows
        ]
    except Exception:
        sql_fallback = text("SELECT * FROM matches")
        rows = db.execute(sql_fallback).mappings().fetchall()
        return [
            {
                "match_id": r.get("match_id", r.get("id")),
                "match_date": str(r.get("match_date", "")),
                "referee": r.get("referee") or "N/A",
                "tournament_id": r.get("tournament_id"),
                "home_team_id": r.get("home_team_id"),
                "away_team_id": r.get("away_team_id"),
                "home_score": r.get("home_score"),
                "away_score": r.get("away_score")
            }
            for r in rows
        ]

@router.post("/")
def create_match(data: MatchSchedule, db: Session = Depends(get_db)):
    ensure_columns_exist(db)
    try:
        m_date = datetime.strptime(data.match_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD expected)")

    sql = text("""
        INSERT INTO matches (tournament_id, home_team_id, away_team_id, match_date, referee)
        VALUES (:t_id, :h_id, :a_id, :m_date, :referee)
    """)
    db.execute(sql, {
        "t_id": data.tournament_id,
        "h_id": data.home_team_id,
        "a_id": data.away_team_id,
        "m_date": m_date,
        "referee": data.referee
    })
    db.commit()
    return {"message": "Match scheduled successfully"}

@router.put("/{match_id}/score")
@router.post("/{match_id}/score")
def update_score(match_id: int, data: MatchScore, db: Session = Depends(get_db)):
    ensure_columns_exist(db)
    
    # Met à jour le score indépendamment du nom de la clé primaire (match_id ou id)
    try:
        sql = text("UPDATE matches SET home_score = :h_score, away_score = :a_score WHERE match_id = :m_id")
        res = db.execute(sql, {"h_score": data.home_score, "a_score": data.away_score, "m_id": match_id})
        if res.rowcount == 0:
            sql_alt = text("UPDATE matches SET home_score = :h_score, away_score = :a_score WHERE id = :m_id")
            db.execute(sql_alt, {"h_score": data.home_score, "a_score": data.away_score, "m_id": match_id})
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Score updated successfully"}
