import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/football_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Générateur de session SQLAlchemy"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Alias pour compatibilité avec le code existant
get_db_connection = get_db

def test_connection():
    """Vérifie la connexion à la base de données"""
    try:
        with engine.connect() as connection:
            return "connected"
    except Exception as e:
        return f"error: {str(e)}"
