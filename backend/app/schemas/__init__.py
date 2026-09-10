from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int
    created_at: Optional[date] = None

    class Config:
        from_attributes = True

# --- Tournament Schemas ---
class TournamentBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    organizer_id: int

class TournamentCreate(TournamentBase):
    pass

class Tournament(TournamentBase):
    tournament_id: int
    created_at: Optional[date] = None

    class Config:
        from_attributes = True

# --- Team Schemas ---
class TeamBase(BaseModel):
    name: str
    coach: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    team_id: int

    class Config:
        from_attributes = True

# --- Player Schemas ---
class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    position: Optional[str] = None
    team_id: int

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    player_id: int

    class Config:
        from_attributes = True

# --- Match Schemas ---
class MatchBase(BaseModel):
    match_date: date
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    tournament_id: int
    home_team_id: int
    away_team_id: int

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    match_id: int
    created_at: Optional[date] = None

    class Config:
        from_attributes = True

# --- TeamTournament Schemas ---
class TeamTournamentBase(BaseModel):
    team_id: int
    tournament_id: int

class TeamTournament(TeamTournamentBase):
    class Config:
        from_attributes = True

# --- Ranking Schemas ---
class RankingItem(BaseModel):
    position: int
    team_name: str
    matches_played: int
    goals_scored: int
    goals_conceded: int
    points: int

class TournamentRanking(BaseModel):
    tournament: str
    ranking: List[RankingItem]
