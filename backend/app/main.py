import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.routes import teams, tournaments, matches
from app.database import test_connection

app = fastapi.FastAPI(
    title="Football Tournament Management System",
    description="REST API for managing football tournaments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "db": test_connection()}

@app.get("/")
def root():
    return {"message": "Welcome to Football Tournament API", "db_status": test_connection()}

# Ingestion des routes sans restriction de token
app.include_router(tournaments.router, prefix="/tournaments", tags=["Tournaments"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(matches.router, prefix="/matches", tags=["Matches"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
