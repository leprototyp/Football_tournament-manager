from datetime import date
from app.database import SessionLocal, engine
from app import models

# Assure la création des tables
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # 1. Créer un organisateur
    user = models.User(
        username="organizer1",
        email="org@example.com",
        password="hashedpassword123",
        role="admin"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2. Créer deux équipes
    team1 = models.Team(name="Paris SG", coach="Luis Enrique")
    team2 = models.Team(name="Real Madrid", coach="Carlo Ancelotti")
    db.add_all([team1, team2])
    db.commit()
    db.refresh(team1)
    db.refresh(team2)

    # 3. Créer un tournoi
    tournament = models.Tournament(
        name="Champions Cup 2026",
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 15),
        organizer_id=user.user_id
    )
    db.add(tournament)
    db.commit()
    db.refresh(tournament)

    # 4. Créer un match
    match = models.Match(
        match_date=date(2026, 9, 5),
        home_score=2,
        away_score=1,
        tournament_id=tournament.tournament_id,
        home_team_id=team1.team_id,
        away_team_id=team2.team_id
    )
    db.add(match)
    db.commit()

    print("Données de test insérées avec succès !")

except Exception as e:
    print(f"Erreur lors de l'insertion : {e}")
    db.rollback()
finally:
    db.close()
