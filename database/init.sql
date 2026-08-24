-- ============================================================
-- Football Tournament Management System
-- Script d'initialisation de la base de données
-- Handout 2-5 : ER-Modell → Schéma relationnel → SQL DDL
-- ============================================================

-- 1. Supprimer les tables si elles existent (ordre inverse des dépendances)
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS team_tournaments CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. Création des tables (Handout 5, §2.2)

-- Table User (Handout 2, §2.1)
CREATE TABLE users (
    user_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,           -- Handout 5, §2.3.4 (UNIQUE)
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,                 -- Stocké hashé !
    role VARCHAR(20) NOT NULL CHECK (role IN ('organizer', 'player', 'viewer')),  -- Handout 5, §2.3.5 (CHECK)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table Tournament (Handout 2, §2.1)
CREATE TABLE tournaments (
    tournament_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,                       -- Handout 5, §2.1.3 (DATE)
    end_date DATE NOT NULL,
    organizer_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES users(user_id)  -- Handout 5, §2.3.2
        ON DELETE RESTRICT                          -- Handout 5, §2.3.2 (RESTRICT)
        ON UPDATE CASCADE,
    CHECK (start_date <= end_date)                  -- Handout 5, §2.3.5 (CHECK)
);

-- Table Team
CREATE TABLE teams (
    team_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    coach VARCHAR(100)
);

-- Table Player
CREATE TABLE players (
    player_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(30),
    team_id INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON DELETE CASCADE                           -- Handout 5, §2.3.2 (CASCADE)
        ON UPDATE CASCADE
);

-- Table Match
CREATE TABLE matches (
    match_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    match_date DATE NOT NULL,
    home_score INTEGER DEFAULT 0 CHECK (home_score >= 0),
    away_score INTEGER DEFAULT 0 CHECK (away_score >= 0),
    tournament_id INTEGER NOT NULL,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK (home_team_id != away_team_id)            -- Une équipe ne peut pas jouer contre elle-même
);

-- Table d'association N:M (Handout 2, §3.3)
CREATE TABLE team_tournaments (
    team_id INTEGER NOT NULL,
    tournament_id INTEGER NOT NULL,
    PRIMARY KEY (team_id, tournament_id),           -- Clé composée (Handout 3, §2.1)
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 3. Création des index pour optimiser les performances (Handout 6)
CREATE INDEX idx_matches_tournament ON matches(tournament_id);
CREATE INDEX idx_matches_home_team ON matches(home_team_id);
CREATE INDEX idx_matches_away_team ON matches(away_team_id);
CREATE INDEX idx_players_team ON players(team_id);
CREATE INDEX idx_tournaments_organizer ON tournaments(organizer_id);

-- 4. Affichage des tables créées
\dt
