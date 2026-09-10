import requests
import tkinter as tk
from tkinter import ttk, messagebox
from football_tournament import api

class CreateTournamentForm(tk.Toplevel):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        self.title("Create New Tournament")
        self.geometry("400x320")
        self.resizable(False, False)
        self.on_success_callback = on_success_callback
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Tournament Name:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_name = ttk.Entry(frame, width=40)
        self.entry_name.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Start Date (YYYY-MM-DD):", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_start = ttk.Entry(frame, width=40)
        self.entry_start.insert(0, "2026-09-01")
        self.entry_start.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="End Date (YYYY-MM-DD):", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_end = ttk.Entry(frame, width=40)
        self.entry_end.insert(0, "2026-09-15")
        self.entry_end.pack(fill="x", pady=(0, 15))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame, text="Create Tournament", command=self.submit).pack(side="right", expand=True, padx=5)

    def submit(self):
        name = self.entry_name.get().strip()
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()

        if not name or not start or not end:
            messagebox.showerror("Error", "All fields are required!", parent=self)
            return

        try:
            api.create_tournament(name, start, end)
            messagebox.showinfo("Success", f"Tournament '{name}' created successfully!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", f"Could not create tournament:\n{e}", parent=self)


class CreateTeamForm(tk.Toplevel):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        self.title("Add New Team")
        self.geometry("400x260")
        self.resizable(False, False)
        self.on_success_callback = on_success_callback
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Team Name:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_team_name = ttk.Entry(frame, width=40)
        self.entry_team_name.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Coach / Manager Name:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_coach_name = ttk.Entry(frame, width=40)
        self.entry_coach_name.pack(fill="x", pady=(0, 15))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame, text="Add Team", command=self.submit).pack(side="right", expand=True, padx=5)

    def submit(self):
        team_name = self.entry_team_name.get().strip()
        coach_name = self.entry_coach_name.get().strip()

        if not team_name or not coach_name:
            messagebox.showerror("Error", "All fields are required!", parent=self)
            return

        try:
            api.create_team(name=team_name, coach_name=coach_name)
            messagebox.showinfo("Success", f"Team '{team_name}' added successfully!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", f"Could not add team:\n{e}", parent=self)


class ScheduleMatchForm(tk.Toplevel):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        self.title("Schedule Match")
        self.geometry("400x450")
        self.resizable(False, False)
        self.on_success_callback = on_success_callback
        self.transient(parent)
        self.grab_set()

        self.teams_map = {}
        team_names = []
        try:
            teams = api.get_teams()
            for t in teams:
                t_id = t.get("team_id")
                t_name = t.get("name")
                if t_id and t_name:
                    display_str = str(t_name)
                    self.teams_map[display_str] = t_id
                    team_names.append(display_str)
        except Exception as e:
            messagebox.showerror("Error", "Could not load teams: " + str(e), parent=self)

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Tournament:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        
        try:
            tournaments_list = api.get_tournaments() if hasattr(api, 'get_tournaments') else requests.get(f"{API_URL}/tournaments/", headers=api.get_headers()).json()
        except Exception as e:
            print('Erreur chargement tournois:', e)
            tournaments_list = []
            
        self.tournament_dict = {t.get('name', 'Tournoi'): (t.get('tournament_id') or t.get('id')) for t in tournaments_list}
        tournament_names = list(self.tournament_dict.keys())
        
        self.tournament_combobox = ttk.Combobox(frame, values=tournament_names, width=38, state="readonly")
        self.tournament_combobox.pack(fill="x", pady=(0, 10))
        if tournament_names:
            self.tournament_combobox.current(0)

        ttk.Label(frame, text="Match Date (YYYY-MM-DD):", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_date = ttk.Entry(frame, width=40)
        self.entry_date.insert(0, "2026-09-10")
        self.entry_date.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Home Team:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.combo_home = ttk.Combobox(frame, values=team_names, state="readonly", width=38)
        self.combo_home.pack(fill="x", pady=(0, 10))
        if team_names:
            self.combo_home.current(0)

        ttk.Label(frame, text="Away Team:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.combo_away = ttk.Combobox(frame, values=team_names, state="readonly", width=38)
        self.combo_away.pack(fill="x", pady=(0, 10))
        if len(team_names) > 1:
            self.combo_away.current(1)
        elif team_names:
            self.combo_away.current(0)

        ttk.Label(frame, text="Referee Name:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_referee = ttk.Entry(frame, width=40)
        self.entry_referee.pack(fill="x", pady=(0, 15))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame, text="Schedule Match", command=self.submit).pack(side="right", expand=True, padx=5)

    def submit(self):
        t_id = str(self.tournament_dict.get(self.tournament_combobox.get(), ""))
        m_date = self.entry_date.get().strip()
        home_sel = self.combo_home.get()
        away_sel = self.combo_away.get()
        referee = self.entry_referee.get().strip()

        if not t_id or not m_date or not home_sel or not away_sel or not referee:
            messagebox.showerror("Error", "All fields are required!", parent=self)
            return

        home_id = self.teams_map.get(home_sel)
        away_id = self.teams_map.get(away_sel)

        if home_id == away_id:
            messagebox.showerror("Error", "Home Team and Away Team must be different!", parent=self)
            return

        try:
            api.create_match_scheduled(int(t_id), int(home_id), int(away_id), m_date, referee)
            messagebox.showinfo("Success", "Match scheduled successfully!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", "Could not schedule match: " + str(e), parent=self)


class UpdateScoreForm(tk.Toplevel):
    def __init__(self, parent, match_id, home_team, away_team, on_success_callback):
        super().__init__(parent)
        self.title("Enter Match Result")
        self.geometry("380x240")
        self.resizable(False, False)
        self.match_id = match_id
        self.home_team = home_team
        self.away_team = away_team
        self.on_success_callback = on_success_callback
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        # Match Title Header
        title_text = f"Match #{match_id}: {home_team} vs {away_team}"
        ttk.Label(frame, text=title_text, font=("Helvetica", 11, "bold")).pack(anchor="center", pady=(0, 20))

        # Horizontal Layout for Home Score - Away Score
        score_frame = ttk.Frame(frame)
        score_frame.pack(anchor="center", pady=(0, 25))

        # Home Team Block
        home_box = ttk.Frame(score_frame)
        home_box.pack(side="left", padx=15)
        ttk.Label(home_box, text=home_team, font=("Helvetica", 10)).pack(anchor="center", pady=(0, 5))
        self.entry_home = ttk.Entry(home_box, width=5, justify="center", font=("Helvetica", 10))
        self.entry_home.pack(anchor="center")

        # Dash Separator
        ttk.Label(score_frame, text="-", font=("Helvetica", 12, "bold")).pack(side="left", padx=10)

        # Away Team Block
        away_box = ttk.Frame(score_frame)
        away_box.pack(side="left", padx=15)
        ttk.Label(away_box, text=away_team, font=("Helvetica", 10)).pack(anchor="center", pady=(0, 5))
        self.entry_away = ttk.Entry(away_box, width=5, justify="center", font=("Helvetica", 10))
        self.entry_away.pack(anchor="center")

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(anchor="center")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Save Result", command=self.submit).pack(side="left", padx=10)

    def submit(self):
        h_score = self.entry_home.get().strip()
        a_score = self.entry_away.get().strip()

        if not h_score.isdigit() or not a_score.isdigit():
            messagebox.showerror("Error", "Scores must be valid integers!", parent=self)
            return

        try:
            api.update_score(self.match_id, int(h_score), int(a_score))
            messagebox.showinfo("Success", "Score updated successfully!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", "Could not update score: " + str(e), parent=self)


        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"Match ID: {match_id}", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 10))

        ttk.Label(frame, text="Home Score:").pack(anchor="w", pady=(0, 2))
        self.entry_home = ttk.Entry(frame, width=30)
        self.entry_home.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Away Score:").pack(anchor="w", pady=(0, 2))
        self.entry_away = ttk.Entry(frame, width=30)
        self.entry_away.pack(fill="x", pady=(0, 15))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame, text="Save Score", command=self.submit).pack(side="right", expand=True, padx=5)

    def submit(self):
        h_score = self.entry_home.get().strip()
        a_score = self.entry_away.get().strip()

        if not h_score.isdigit() or not a_score.isdigit():
            messagebox.showerror("Error", "Scores must be valid integers!", parent=self)
            return

        try:
            api.update_score(self.match_id, int(h_score), int(a_score))
            messagebox.showinfo("Success", "Score updated successfully!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", "Could not update score: " + str(e), parent=self)


class TournamentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Football Tournament Manager")
        self.geometry("950x650")

        self.is_organizer = False
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        login_frame = ttk.Frame(self.main_container, padding="30")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(login_frame, text="🏆 System Login", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        ttk.Label(login_frame, text="Backend URL:").pack(anchor="w", pady=(5, 2))
        self.entry_url = ttk.Entry(login_frame, width=40)
        self.entry_url.insert(0, "http://localhost:8000")
        self.entry_url.pack(pady=(0, 10))

        ttk.Label(login_frame, text="Organizer Key (Optional):").pack(anchor="w", pady=(5, 2))
        self.entry_key = ttk.Entry(login_frame, width=40, show="*")
        self.entry_key.insert(0, "mykey")
        self.entry_key.pack(pady=(0, 20))

        ttk.Button(login_frame, text="Connect", command=self.handle_login).pack(fill="x")

    def handle_login(self):
        url = self.entry_url.get().strip()
        key = self.entry_key.get().strip()

        api.set_config(url, key)

        if api.check_health():
            self.is_organizer = (key == "mykey")
            self.show_dashboard()
        else:
            messagebox.showerror("Connection Error", "Could not connect to FastAPI server.")

    def show_dashboard(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        header = ttk.Frame(self.main_container, padding="10")
        header.pack(fill="x")

        role_txt = "🛠️ Organizer Mode" if self.is_organizer else "👁️ Viewer Mode"
        ttk.Label(header, text=f"Football Manager - {role_txt}", font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Logout", command=self.show_login_screen).pack(side="right", padx=5)
        ttk.Button(header, text="🔄 Refresh Data", command=self.refresh_all).pack(side="right", padx=5)

        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab_tournaments = ttk.Frame(self.notebook, padding="10")
        self.tab_teams = ttk.Frame(self.notebook, padding="10")
        self.tab_matches = ttk.Frame(self.notebook, padding="10")
        self.tab_standings = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.tab_tournaments, text="🏆 Tournaments")
        self.notebook.add(self.tab_teams, text="⚽ Teams")
        self.notebook.add(self.tab_matches, text="📅 Matches")
        self.notebook.add(self.tab_standings, text="📊 Standings")

        self.setup_tournaments_tab()
        self.setup_teams_tab()
        self.setup_matches_tab()
        self.setup_standings_tab()

        self.refresh_all()

    
    def delete_selected_tournament(self):
        selected_item = self.tree_tournaments.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a tournament to delete.")
            return
        item_data = self.tree_tournaments.item(selected_item)
        values = item_data.get("values", [])
        if not values:
            return
        tournament_id = values[0]
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this tournament?"):
            try:
                response = requests.delete(f"http://localhost:8000/tournaments/{tournament_id}")
                if response.status_code in [200, 204]:
                    messagebox.showinfo("Success", "Tournament deleted successfully.")
                    self.refresh_all()
                else:
                    messagebox.showerror("Error", f"Erreur serveur : {response.status_code}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Unable to connect to the FastAPI server.")


    def setup_tournaments_tab(self):
        if self.is_organizer:
            top_bar = ttk.Frame(self.tab_tournaments)
            top_bar.pack(fill="x", pady=(0, 10))
            ttk.Button(top_bar, text="+ New Tournament", command=lambda: CreateTournamentForm(self, self.refresh_all)).pack(side="left", padx=(0, 5))
            ttk.Button(top_bar, text="Delete", command=self.delete_selected_tournament).pack(side="left")

        self.tree_tournaments = ttk.Treeview(self.tab_tournaments, columns=("ID", "Name", "Start", "End"), show="headings")
        for col, h in [("ID", "ID"), ("Name", "Tournament Name"), ("Start", "Start Date"), ("End", "End Date")]:
            self.tree_tournaments.heading(col, text=h)
            self.tree_tournaments.column(col, anchor="center")
        self.tree_tournaments.pack(fill="both", expand=True)

    
    def delete_selected_team(self):
        selected_item = self.tree_teams.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a team to delete.")
            return
        item_data = self.tree_teams.item(selected_item)
        values = item_data.get("values", [])
        if not values:
            return
        team_id = values[0]
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this team?"):
            try:
                response = requests.delete(f"http://localhost:8000/teams/{team_id}")
                if response.status_code in [200, 204]:
                    messagebox.showinfo("Success", "Team deleted successfully.")
                    self.refresh_all()
                else:
                    messagebox.showerror("Error", f"Server error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Unable to connect to the FastAPI server.")


    def setup_teams_tab(self):
        if self.is_organizer:
            top_bar = ttk.Frame(self.tab_teams)
            top_bar.pack(fill="x", pady=(0, 10))
            ttk.Button(top_bar, text="+ Add Team", command=lambda: CreateTeamForm(self, self.refresh_all)).pack(side="left", padx=(0, 5))
            ttk.Button(top_bar, text="Delete", command=self.delete_selected_team).pack(side="left")

        self.tree_teams = ttk.Treeview(self.tab_teams, columns=("ID", "Name", "Coach"), show="headings")
        for col, h in [("ID", "ID"), ("Name", "Team Name"), ("Coach", "Coach / Manager")]:
            self.tree_teams.heading(col, text=h)
            self.tree_teams.column(col, anchor="center")
        self.tree_teams.pack(fill="both", expand=True)

    
    def delete_selected_match(self):
        selected_item = self.tree_matches.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a match to delete.")
            return
        item_data = self.tree_matches.item(selected_item)
        values = item_data.get("values", [])
        if not values:
            return
        match_id = values[0]
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this match?"):
            try:
                response = requests.delete(f"http://localhost:8000/matches/{match_id}")
                if response.status_code in [200, 204]:
                    messagebox.showinfo("Success", "Match deleted successfully.")
                    self.refresh_all()
                else:
                    messagebox.showerror("Error", f"Server error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                messagebox.showerror("Error", "Unable to connect to the FastAPI server.")


    def setup_matches_tab(self):
        top_bar = ttk.Frame(self.tab_matches)
        ttk.Label(top_bar, text="Tournament:").pack(side="left", padx=(0, 5))
        self.matches_tournament_cb = ttk.Combobox(top_bar, state="readonly", width=20)
        self.matches_tournament_cb.pack(side="left", padx=(0, 10))
        self.matches_tournament_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_matches_tab_content())
        top_bar.pack(fill="x", pady=(0, 10))
        if self.is_organizer:
            ttk.Button(top_bar, text="+ Schedule Match", command=lambda: ScheduleMatchForm(self, self.refresh_all)).pack(side="left", padx=(0, 5))
            ttk.Button(top_bar, text="✏️ Update Score", command=self.open_update_score).pack(side="left", padx=(0, 5))
            ttk.Button(top_bar, text="Delete", command=self.delete_selected_match).pack(side="left")

        self.tree_matches = ttk.Treeview(self.tab_matches, columns=("ID", "Date", "Home", "Score", "Away", "Referee"), show="headings")
        for col, h in [("ID", "ID"), ("Date", "Match Date"), ("Home", "Home Team"), ("Score", "Score / Result"), ("Away", "Away Team"), ("Referee", "Referee")]:
            self.tree_matches.heading(col, text=h)
            self.tree_matches.column(col, anchor="center")
        self.tree_matches.pack(fill="both", expand=True)

    def open_update_score(self):
        selected = self.tree_matches.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a match from the list first!")
            return
        item_values = self.tree_matches.item(selected[0])["values"]
        match_id = item_values[0]
        home_team = str(item_values[2])
        away_team = str(item_values[4])
        UpdateScoreForm(self, match_id, home_team, away_team, self.refresh_all)

    
    


    



    def refresh_matches_tab_content(self):
        selected_name = getattr(self, 'matches_tournament_cb', None) and self.matches_tournament_cb.get()
        tournament_id = getattr(self, 'tournament_map', {}).get(selected_name)
        
        for item in self.tree_matches.get_children():
            self.tree_matches.delete(item)
            
        try:
            # Récupérer tous les matchs sans passer tournament_id en paramètre API
            matches = api.get_matches()
            
            for m in matches:
                # Filtrer en Python si un tournoi spécifique est sélectionné
                m_tid = m.get('tournament_id') if isinstance(m, dict) else getattr(m, 'tournament_id', None)
                if tournament_id is not None and m_tid != tournament_id:
                    continue
                
                mid = m.get('match_id') or m.get('id', '')
                mdate = m.get('match_date') or m.get('date', '')
                
                home_id = m.get('home_team_id') or m.get('home_team')
                away_id = m.get('away_team_id') or m.get('away_team')
                
                # Résolution des noms d'équipes via team_map avec fallback sur l'ID ou le nom brut
                team_map = getattr(self, 'team_map', {})
                home_name = team_map.get(home_id) or team_map.get(str(home_id)) or m.get('home_team_name') or str(home_id or '')
                away_name = team_map.get(away_id) or team_map.get(str(away_id)) or m.get('away_team_name') or str(away_id or '')
                
                h_score = m.get('home_score', '-')
                a_score = m.get('away_score', '-')
                score = f"{h_score if h_score is not None else '-'} - {a_score if a_score is not None else '-'}"
                
                referee = m.get('referee') or 'N/A'
                self.tree_matches.insert('', 'end', values=(mid, mdate, home_name, score, away_name, referee))
        except Exception as e:
            print("Erreur filtre matches :", e)

    def refresh_standings_tab_content(self):
        selected_name = getattr(self, 'standings_tournament_cb', None) and self.standings_tournament_cb.get()
        raw_tid = getattr(self, 'tournament_map', {}).get(selected_name)
        try:
            tournament_id = int(raw_tid) if raw_tid is not None else None
        except (TypeError, ValueError):
            tournament_id = None
        
        for item in self.tree_standings.get_children():
            self.tree_standings.delete(item)
        
        try:
            teams = {int(t.get("team_id")): t.get("name") for t in api.get_teams() if t.get("team_id") is not None}
            stats = {}
            for t_id, t_name in teams.items():
                stats[t_id] = {
                    "name": t_name, "played": 0, "won": 0, "drawn": 0, "lost": 0,
                    "gf": 0, "ga": 0, "gd": 0, "pts": 0
                }

            matches = api.get_matches()
            for m in matches:
                m_tid = m.get("tournament_id")
                if tournament_id is not None and m_tid != tournament_id:
                    continue
                
                h_score = m.get("home_score")
                a_score = m.get("away_score")
                try:
                    h_id = int(m.get("home_team_id"))
                    a_id = int(m.get("away_team_id"))
                except (TypeError, ValueError):
                    continue

                if h_score is not None and a_score is not None and h_id in stats and a_id in stats:
                    stats[h_id]["played"] += 1
                    stats[a_id]["played"] += 1
                    stats[h_id]["gf"] += h_score
                    stats[h_id]["ga"] += a_score
                    stats[a_id]["gf"] += a_score
                    stats[a_id]["ga"] += h_score

                    if h_score > a_score:
                        stats[h_id]["won"] += 1
                        stats[h_id]["pts"] += 3
                        stats[a_id]["lost"] += 1
                    elif a_score > h_score:
                        stats[a_id]["won"] += 1
                        stats[a_id]["pts"] += 3
                        stats[h_id]["lost"] += 1
                    else:
                        stats[h_id]["drawn"] += 1
                        stats[a_id]["drawn"] += 1
                        stats[h_id]["pts"] += 1
                        stats[a_id]["pts"] += 1

            for s in stats.values():
                s["gd"] = s["gf"] - s["ga"]

            sorted_teams = sorted(
                stats.values(),
                key=lambda x: (x["pts"], x["gd"], x["gf"]),
                reverse=True
            )

            for idx, s in enumerate(sorted_teams, 1):
                self.tree_standings.insert("", "end", values=(
                    idx, s["name"], s["played"], s["won"], s["drawn"], s["lost"],
                    s["gf"], s["ga"], f"{s['gd']:+d}" if s["gd"] != 0 else "0", s["pts"]
                ))
        except Exception as e:
            print("Error loading standings:", e)

    def load_tournaments_into_combos(self):
        try:
            # Charger d'abord les équipes pour construire team_map de manière fiable
            teams = api.get_teams()
            self.team_map = {}
            for t in teams:
                if isinstance(t, dict):
                    tid = t.get('id') or t.get('team_id')
                    tname = t.get('name')
                else:
                    tid = getattr(t, 'id', getattr(t, 'team_id', None))
                    tname = getattr(t, 'name', str(t))
                if tid is not None:
                    self.team_map[int(tid)] = tname
                    self.team_map[str(tid)] = tname

            tournaments = api.get_tournaments()
            t_names = ["All Tournaments"]
            self.tournament_map = {"All Tournaments": None}
            for t in tournaments:
                if isinstance(t, dict):
                    name = t.get('name')
                    tid = t.get('id') or t.get('tournament_id')
                else:
                    name = getattr(t, 'name', str(t))
                    tid = getattr(t, 'id', getattr(t, 'tournament_id', None))
                if name:
                    t_names.append(name)
                    self.tournament_map[name] = tid
            
            if hasattr(self, 'matches_tournament_cb'):
                self.matches_tournament_cb['values'] = t_names
                if not self.matches_tournament_cb.get() or self.matches_tournament_cb.get() not in t_names:
                    self.matches_tournament_cb.set("All Tournaments")
                    
            if hasattr(self, 'standings_tournament_cb'):
                self.standings_tournament_cb['values'] = t_names
                if not self.standings_tournament_cb.get() or self.standings_tournament_cb.get() not in t_names:
                    self.standings_tournament_cb.set("All Tournaments")
        except Exception as e:
            print("Erreur lors du chargement des données de référence :", e)

    def refresh_all(self):
        self.load_tournaments_into_combos()
        self.load_standings()
        # Load Tournaments
        for item in self.tree_tournaments.get_children():
            self.tree_tournaments.delete(item)
        try:
            for t in api.get_tournaments():
                self.tree_tournaments.insert("", "end", values=(t.get("tournament_id"), t.get("name"), t.get("start_date"), t.get("end_date")))
        except Exception:
            pass

        # Load Teams
        for item in self.tree_teams.get_children():
            self.tree_teams.delete(item)
        try:
            for item in api.get_teams():
                coach = item.get("coach_name") or item.get("manager_name") or item.get("coach") or "N/A"
                self.tree_teams.insert("", "end", values=(item.get("team_id"), item.get("name"), coach))
        except Exception:
            pass

        # Load Matches (respecting selected tournament filter)
        self.refresh_matches_tab_content()



    def setup_standings_tab(self):
        standings_top_frame = ttk.Frame(self.tab_standings)
        standings_top_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(standings_top_frame, text="Tournament:").pack(side="left", padx=(0, 5))
        self.standings_tournament_cb = ttk.Combobox(standings_top_frame, state="readonly", width=20)
        self.standings_tournament_cb.pack(side="left", padx=(0, 10))
        self.standings_tournament_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_standings_tab_content())
        columns = ("Rank", "Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts")
        self.tree_standings = ttk.Treeview(self.tab_standings, columns=columns, show="headings")
        
        headers = {
            "Rank": "#",
            "Team": "Team",
            "P": "Played",
            "W": "Won",
            "D": "Drawn",
            "L": "Lost",
            "GF": "GF",
            "GA": "GA",
            "GD": "GD",
            "Pts": "Points"
        }
        
        col_widths = {
            "Rank": 40,
            "Team": 180,
            "P": 60,
            "W": 50,
            "D": 50,
            "L": 50,
            "GF": 50,
            "GA": 50,
            "GD": 60,
            "Pts": 70
        }

        for col in columns:
            self.tree_standings.heading(col, text=headers[col])
            self.tree_standings.column(col, anchor="center", width=col_widths[col])
        
        self.tree_standings.pack(fill="both", expand=True)

    def load_standings(self):
        for item in self.tree_standings.get_children():
            self.tree_standings.delete(item)
        
        try:
            teams = {int(t.get("team_id")): t.get("name") for t in api.get_teams() if t.get("team_id") is not None}
            stats = {}
            for t_id, t_name in teams.items():
                stats[t_id] = {
                    "name": t_name,
                    "played": 0,
                    "won": 0,
                    "drawn": 0,
                    "lost": 0,
                    "gf": 0,
                    "ga": 0,
                    "gd": 0,
                    "pts": 0
                }

            matches = api.get_matches()
            for m in matches:
                h_score = m.get("home_score")
                a_score = m.get("away_score")
                try:
                    h_id = int(m.get("home_team_id"))
                    a_id = int(m.get("away_team_id"))
                except (TypeError, ValueError):
                    continue

                if h_score is not None and a_score is not None and h_id in stats and a_id in stats:
                    stats[h_id]["played"] += 1
                    stats[a_id]["played"] += 1
                    stats[h_id]["gf"] += h_score
                    stats[h_id]["ga"] += a_score
                    stats[a_id]["gf"] += a_score
                    stats[a_id]["ga"] += h_score

                    if h_score > a_score:
                        stats[h_id]["won"] += 1
                        stats[h_id]["pts"] += 3
                        stats[a_id]["lost"] += 1
                    elif a_score > h_score:
                        stats[a_id]["won"] += 1
                        stats[a_id]["pts"] += 3
                        stats[h_id]["lost"] += 1
                    else:
                        stats[h_id]["drawn"] += 1
                        stats[a_id]["drawn"] += 1
                        stats[h_id]["pts"] += 1
                        stats[a_id]["pts"] += 1

            for s in stats.values():
                s["gd"] = s["gf"] - s["ga"]

            sorted_teams = sorted(
                stats.values(),
                key=lambda x: (x["pts"], x["gd"], x["gf"]),
                reverse=True
            )

            for idx, s in enumerate(sorted_teams, 1):
                self.tree_standings.insert("", "end", values=(
                    idx,
                    s["name"],
                    s["played"],
                    s["won"],
                    s["drawn"],
                    s["lost"],
                    s["gf"],
                    s["ga"],
                    f"{s['gd']:+d}" if s["gd"] != 0 else "0",
                    s["pts"]
                ))
        except Exception as e:
            print("Error loading standings:", e)

if __name__ == "__main__":
    app = TournamentApp()
    app.mainloop()






    def refresh_matches_tab_content(self):
        selected_name = getattr(self, 'matches_tournament_cb', None) and self.matches_tournament_cb.get()
        tournament_id = getattr(self, 'tournament_map', {}).get(selected_name)
        
        for item in self.tree_matches.get_children():
            self.tree_matches.delete(item)
            
        try:
            # Récupérer tous les matchs sans passer tournament_id en paramètre API
            matches = api.get_matches()
            
            for m in matches:
                # Filtrer en Python si un tournoi spécifique est sélectionné
                m_tid = m.get('tournament_id') if isinstance(m, dict) else getattr(m, 'tournament_id', None)
                if tournament_id is not None and m_tid != tournament_id:
                    continue
                
                mid = m.get('match_id') or m.get('id', '')
                mdate = m.get('match_date') or m.get('date', '')
                
                home_id = m.get('home_team_id') or m.get('home_team')
                away_id = m.get('away_team_id') or m.get('away_team')
                
                # Résolution des noms d'équipes via team_map avec fallback sur l'ID ou le nom brut
                team_map = getattr(self, 'team_map', {})
                home_name = team_map.get(home_id) or team_map.get(str(home_id)) or m.get('home_team_name') or str(home_id or '')
                away_name = team_map.get(away_id) or team_map.get(str(away_id)) or m.get('away_team_name') or str(away_id or '')
                
                h_score = m.get('home_score', '-')
                a_score = m.get('away_score', '-')
                score = f"{h_score if h_score is not None else '-'} - {a_score if a_score is not None else '-'}"
                
                referee = m.get('referee') or 'N/A'
                self.tree_matches.insert('', 'end', values=(mid, mdate, home_name, score, away_name, referee))
        except Exception as e:
            print("Erreur filtre matches :", e)

