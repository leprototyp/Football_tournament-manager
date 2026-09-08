from sqlalchemy import Column, Integer, String, Date, ForeignKey, CheckConstraint, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, Identity(start=1), primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(Date, server_default=func.now())
    
    tournaments = relationship("Tournament", back_populates="organizer")

class Tournament(Base):
    __tablename__ = "tournaments"
    
    tournament_id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(Date, server_default=func.now())
    
    organizer = relationship("User", back_populates="tournaments")
    teams = relationship("TeamTournament", back_populates="tournament")
    matches = relationship("Match", back_populates="tournament")

class Team(Base):
    __tablename__ = "teams"
    
    team_id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    coach = Column(String(100))
    
    players = relationship("Player", back_populates="team")
    tournaments = relationship("TeamTournament", back_populates="team")
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")

class Player(Base):
    __tablename__ = "players"
    
    player_id = Column(Integer, Identity(start=1), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position = Column(String(30))
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    
    team = relationship("Team", back_populates="players")

class Match(Base):
    __tablename__ = "matches"
    
    match_id = Column(Integer, Identity(start=1), primary_key=True)
    match_date = Column(Date, nullable=False)
    referee = Column(String, nullable=True)
    home_score = Column(Integer, default=0)
    away_score = Column(Integer, default=0)
    tournament_id = Column(Integer, ForeignKey("tournaments.tournament_id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    created_at = Column(Date, server_default=func.now())
    
    tournament = relationship("Tournament", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")

class TeamTournament(Base):
    __tablename__ = "team_tournaments"
    
    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.tournament_id"), primary_key=True)
    
    team = relationship("Team", back_populates="tournaments")
    tournament = relationship("Tournament", back_populates="teams")
