# ⚽ Football Tournament Management System

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 Overview

**Football Tournament Management System** is a complete platform for organizing and managing football competitions. It provides a seamless experience for tournament organizers, teams, and players to manage tournaments efficiently.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 👥 **Team Management** | Register teams with players and coaches |
| 📅 **Match Scheduling** | Create and manage match schedules |
| 📊 **Live Rankings** | Automatic ranking calculation based on results |
| 🔐 **User Roles** | Organizers, players, and viewers with different permissions |
| 🖥️ **Desktop Interface** | User-friendly Tkinter desktop application |
| 🚀 **REST API** | Comprehensive FastAPI backend with Swagger documentation |
| 🐳 **Docker Ready** | Easy deployment with Docker Compose |

---

## 🏗️ Architecture

The system consists of three main components:
┌─────────────────────────────────────────────────────────────────┐
│ Football Tournament System │
├─────────────────────────────────────────────────────────────────┤
│ │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ Tkinter │ │ FastAPI │ │ PostgreSQL │ │
│ │ Frontend │◄──►│ Backend │◄──►│ Database │ │
│ │ (Desktop) │ │ (REST API) │ │ │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│ │ │ │ │
│ └───────────────────┼───────────────────┘ │
│ │ │
│ ┌───────▼───────┐ │
│ │ Docker │ │
│ │ Compose │ │
│ └───────────────┘ │
└─────────────────────────────────────────────────────────────────┘

**Docker Compose Services:**
- PostgreSQL (database)
- FastAPI (backend API)

**Frontend:**
- Tkinter desktop application
- Delivered as .deb package

---

## 🚀 Quick Start Guide

### Option 1: With Docker (Recommended for Backend)

```bash
# 1. Clone the repository
git clone https://gitlab.thga.de/rostand.assonfo-demaboi/football-tournament-manager.git
cd football-tournament-manager

# 2. Copy environment variables
cp .env.example .env

# 3. Edit .env file with your configuration
#    Change API_KEY, database credentials, etc.

# 4. Start the backend services
docker-compose up -d

# 5. Access the API
#    - API: http://localhost:8000
#    - API Documentation: http://localhost:8000/docs

## Option 2: Without Docker (Development)

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd frontend
python app.py


📊 API Endpoints

Public Endpoints (No Authentication Required)

Method	Endpoint			Description			SQL Features
GET	/				Welcome message			-
GET	/health				Health check			-
GET	/teams				List all teams			JOIN with players
GET	/tournaments			List all tournaments		-
GET	/tournaments/{id}		Get tournament details		JOIN with organizer
GET	/tournaments/{id}/ranking	Get tournament ranking		AGGREGATION (SUM, COUNT)
GET	/tournaments/{id}/teams		Get teams in a tournament	JOIN (TeamTournament)
GET	/matches			List all matches		JOIN with teams

Protected Endpoints (X-API-Key Required)

Method	Endpoint	Description
POST	/teams		Create a new team
PUT	/teams/{id}	Update team details
DELETE	/teams/{id}	Delete a team
POST	/matches	Create a new match
PUT	/matches/{id}	Update match results
DELETE	/matches/{id}	Delete a match
POST	/tournaments	Create a new tournament

Authentication Example

# Using curl with API key
curl -X POST http://localhost:8000/teams \
  -H "X-API-Key: your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "FC Eagles", "coach": "John Doe"}'

# Using Python requests
import requests
headers = {"X-API-Key": "your-secret-api-key"}
response = requests.post(
    "http://localhost:8000/matches",
    json={
        "home_team_id": 1,
        "away_team_id": 2,
        "match_date": "2026-09-01"
    },
    headers=headers
)

📁 Project Structure

football-tournament-manager/
│
├── backend/                    # FastAPI Backend (Docker container)
│   ├── app/
│   │   ├── models/             # SQLAlchemy database models
│   │   ├── schemas/            # Pydantic validation schemas
│   │   ├── crud/               # CRUD operations
│   │   ├── routes/             # API route handlers
│   │   ├── main.py             # FastAPI application entry point
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database connection
│   │   └── auth.py             # Authentication (X-API-Key)
│   ├── requirements.txt        # Python dependencies
│   ├── requirements-dev.txt    # Development dependencies
│   ├── Dockerfile              # Docker image for backend
│   └── pytest.ini              # Test configuration
│
├── frontend/                   # Tkinter Desktop Application (.deb package)
│   ├── app.py                  # Application entry point
│   ├── api_client.py           # API communication client
│   ├── config.py               # Frontend configuration
│   └── ui/                     # UI components
│       ├── connection_dialog.py   # Startup: API URL + X-API-Key
│       ├── dashboard.py           # Main dashboard (read-only GET)
│       ├── tournament_view.py     # Tournament view
│       ├── team_manager.py        # Team management
│       ├── match_form.py          # Match creation form (POST /matches)
│       └── ranking_view.py        # Tournament ranking display
│
├── database/                   # Database Scripts
│   ├── init.sql                # Initial schema creation
│   ├── seed.sql                # Sample data for testing
│   └── migrations/             # Schema migrations
│
├── tests/                      # Test Suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── conftest.py             # Test configuration
│
├── scripts/                    # Utility scripts
├── docs/                       # Documentation
├── screenshots/                # Application screenshots
│
├── docker-compose.yml          # Docker orchestration (PostgreSQL + FastAPI)
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── LICENSE                     # MIT License
└── README.md                   # This file

Testing

# Run all tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/integration/test_api_teams.py -v

# Test authentication
pytest tests/integration/test_api_auth.py -v

# Run tests with verbose output
pytest -v --tb=short

Test Coverage

# Generate coverage report
pytest --cov=app --cov-report=html tests/
# Open htmlcov/index.html in browser

Docker Commands

# Build and start containers
docker-compose up -d --build

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs fastapi
docker-compose logs postgres

# Stop containers
docker-compose down

# Stop and remove volumes (clear database)
docker-compose down -v

# Restart a service
docker-compose restart fastapi

# Access database shell
docker-compose exec postgres psql -U football_user -d football_tournament

# Check container status
docker-compose ps

 Deployment on University Server
 
 Backend Deployment
 
 # 1. Copy files to server
scp -r football-tournament-manager/ user@server:/path/to/deploy/

# 2. Configure environment
cd /path/to/deploy/football-tournament-manager
cp .env.example .env
# Edit .env with production values

# 3. Start services
docker-compose up -d --build

# 4. Verify deployment
curl http://server-ip:8000/health

Frontend Installation (.deb package)

# Install the frontend
sudo dpkg -i football-tournament-manager.deb

# Launch the application
football-tournament-manager

 Security

    All write operations require a valid X-API-Key header

    API keys are stored in environment variables (not in code)

    Database credentials are managed via .env file

    SQLAlchemy ORM prevents SQL injection

    CORS configured for secure cross-origin requests

Best Practices

    Always use a strong API Key: Generate a secure random key

    Keep .env file private: Never commit it to version control

    Use HTTPS in production: Configure SSL certificates

    Regular backups: Backup your PostgreSQL database
    


Development Setup

Prerequisites

    Python 3.10+

    PostgreSQL 15+

    Docker (optional)

    Git

Development Environment

# Clone the repository
git clone https://gitlab.thga.de/rostand.assonfo-demaboi/football-tournament-manager.git
cd football-tournament-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development

# Run the application
uvicorn app.main:app --reload

Acceptance Criteria

The system is considered complete when:

    ✅ Database correctly stores users, tournaments, teams, players, and matches

    ✅ All primary key and foreign key constraints are enforced

    ✅ API returns correct results for JOIN operations (e.g., teams in a tournament)

    ✅ Tournament ranking endpoint returns correct standings using SQL aggregation

    ✅ Write operations without valid X-API-Key are rejected (HTTP 401/403)

    ✅ Authorized organizers can successfully create and delete match records
    
    
Documentation

    API Documentation: /docs (Swagger UI) and /redoc (ReDoc)

    User Guide: docs/user-guide.md

    Architecture: docs/architecture.md

    Deployment Guide: docs/deployment.md
    
 🤝 Contributing

    Fork the repository

    Create a feature branch (git checkout -b feature/AmazingFeature)

    Commit your changes (git commit -m 'Add some AmazingFeature')

    Push to the branch (git push origin feature/AmazingFeature)

    Open a Merge Request

👨‍💻 Author

Assonfo Demaboi, Rostand Cedrix

    📧 Email: rostand.assonfo-demaboi@stud.thga.de

    🦊 GitLab: @rostand.assonfo-demaboi

    🏛️ University: THGA (Technische Hochschule Georg Agricola)

🙏 Acknowledgments

    FastAPI - Modern web framework for building APIs

    PostgreSQL - Powerful open-source relational database

    Tkinter - Python's standard GUI framework

    Docker - Containerization platform

    SQLAlchemy - SQL toolkit and ORM

📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

Made with ❤️ for the Football Community
