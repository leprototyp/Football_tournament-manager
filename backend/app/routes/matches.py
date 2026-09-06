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

@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    sql = text("SELECT match_id, match_date, referee, tournament_id, home_team_id, away_team_id FROM matches")
    try:
        rows = db.execute(sql).fetchall()
        return [
            {
                "match_id": r[0],
                "match_date": str(r[1]),
                "referee": r[2] if r[2] else "N/A",
                "tournament_id": r[3],
                "home_team_id": r[4],
                "away_team_id": r[5]
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
                "away_team_id": r.get("away_team_id")
            }
            for r in rows
        ]

@router.post("/")
def create_match(data: MatchSchedule, db: Session = Depends(get_db)):
    try:
        m_date = datetime.strptime(data.match_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (YYYY-MM-DD expected)")

    try:
        db.execute(text("ALTER TABLE matches ADD COLUMN referee VARCHAR;"))
        db.commit()
    except Exception:
        db.rollback()

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
