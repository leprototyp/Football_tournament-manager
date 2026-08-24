-- ============================================================
-- Données de test (Handout 5, §3.1)
-- ============================================================

-- 1. Utilisateurs
INSERT INTO users (username, email, password, role) VALUES
('organizer1', 'org1@email.com', 'hashed_password', 'organizer'),
('player1', 'player1@email.com', 'hashed_password', 'player'),
('viewer1', 'viewer1@email.com', 'hashed_password', 'viewer');

-- 2. Tournoi
INSERT INTO tournaments (name, start_date, end_date, organizer_id) VALUES
('THGA Cup 2026', '2026-09-01', '2026-09-30', 1);

-- 3. Équipes
INSERT INTO teams (name, coach) VALUES
('FC Eagles', 'John Coach'),
('Lions FC', 'Sarah Manager'),
('Tigers United', 'Mike Trainer');

-- 4. Association équipes-tournoi (N:M)
INSERT INTO team_tournaments (team_id, tournament_id) VALUES
(1, 1), (2, 1), (3, 1);

-- 5. Joueurs
INSERT INTO players (first_name, last_name, position, team_id) VALUES
('Alice', 'Smith', 'Forward', 1),
('Bob', 'Johnson', 'Midfielder', 1),
('Charlie', 'Brown', 'Defender', 2),
('Diana', 'Prince', 'Goalkeeper', 2),
('Eve', 'Davis', 'Forward', 3),
('Frank', 'Miller', 'Midfielder', 3);

-- 6. Matchs
INSERT INTO matches (match_date, home_score, away_score, tournament_id, home_team_id, away_team_id) VALUES
('2026-09-01', 2, 1, 1, 1, 2),  -- FC Eagles 2-1 Lions FC
('2026-09-03', 0, 0, 1, 2, 3),  -- Lions FC 0-0 Tigers United
('2026-09-05', 3, 0, 1, 3, 1),  -- Tigers United 3-0 FC Eagles
('2026-09-08', 1, 1, 1, 2, 1),  -- Lions FC 1-1 FC Eagles
('2026-09-10', 2, 2, 1, 3, 2),  -- Tigers United 2-2 Lions FC
('2026-09-12', 0, 1, 1, 1, 3);  -- FC Eagles 0-1 Tigers United
