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
        self.geometry("420x440")
        self.resizable(False, False)
        self.on_success_callback = on_success_callback
        self.transient(parent)
        self.grab_set()

        self.teams_map = {}
        try:
            teams = api.get_teams()
            for t in teams:
                name = t.get('name')
                team_id = t.get('team_id')
                if name:
                    self.teams_map[name] = team_id
        except Exception:
            pass

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Tournament ID:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_t_id = ttk.Entry(frame, width=40)
        self.entry_t_id.insert(0, "1")
        self.entry_t_id.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Match Date (YYYY-MM-DD):", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_date = ttk.Entry(frame, width=40)
        self.entry_date.insert(0, "2026-09-18")
        self.entry_date.pack(fill="x", pady=(0, 10))

        team_names = list(self.teams_map.keys())

        ttk.Label(frame, text="Home Team:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.combo_home = ttk.Combobox(frame, values=team_names, state="readonly", width=38)
        self.combo_home.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Away Team:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.combo_away = ttk.Combobox(frame, values=team_names, state="readonly", width=38)
        self.combo_away.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Referee Name:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 2))
        self.entry_referee = ttk.Entry(frame, width=40)
        self.entry_referee.pack(fill="x", pady=(0, 15))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame, text="Schedule Match", command=self.submit).pack(side="right", expand=True, padx=5)

    def submit(self):
        t_id = self.entry_t_id.get().strip()
        m_date = self.entry_date.get().strip()
        home_name = self.combo_home.get()
        away_name = self.combo_away.get()
        referee = self.entry_referee.get().strip()

        if not t_id or not m_date or not home_name or not away_name or not referee:
            messagebox.showerror("Error", "All fields are required!", parent=self)
            return

        home_id = self.teams_map.get(home_name)
        away_id = self.teams_map.get(away_name)

        if home_id == away_id:
            messagebox.showerror("Error", "Home Team and Away Team must be different!", parent=self)
            return

        try:
            api.create_match_scheduled(int(t_id), int(home_id), int(away_id), m_date, referee)
            messagebox.showinfo("Success", "Match scheduled successfully!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", f"Could not schedule match:\n{e}", parent=self)


class UpdateScoreForm(tk.Toplevel):
    def __init__(self, parent, match_id, home_team, away_team, on_success_callback):
        super().__init__(parent)
        self.title("Enter Match Result")
        self.geometry("380x260")
        self.resizable(False, False)
        self.match_id = match_id
        self.on_success_callback = on_success_callback
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding="20")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"Match #{match_id}: {home_team} vs {away_team}", font=("Helvetica", 10, "bold")).pack(pady=(0, 15))

        score_frame = ttk.Frame(frame)
        score_frame.pack(fill="x", pady=10)

        f_home = ttk.Frame(score_frame)
        f_home.pack(side="left", expand=True)
        ttk.Label(f_home, text=home_team).pack()
        self.entry_home = ttk.Entry(f_home, width=5, justify="center")
        self.entry_home.pack(pady=5)
        self.entry_home.insert(0, "0")

        ttk.Label(score_frame, text=" - ", font=("Helvetica", 14, "bold")).pack(side="left")

        f_away = ttk.Frame(score_frame)
        f_away.pack(side="right", expand=True)
        ttk.Label(f_away, text=away_team).pack()
        self.entry_away = ttk.Entry(f_away, width=5, justify="center")
        self.entry_away.pack(pady=5)
        self.entry_away.insert(0, "0")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(20, 0))
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame, text="Save Result", command=self.submit).pack(side="right", expand=True, padx=5)

    def submit(self):
        try:
            h_score = int(self.entry_home.get().strip())
            a_score = int(self.entry_away.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Scores must be valid integers!", parent=self)
            return

        try:
            api.update_match_result(self.match_id, h_score, a_score)
            messagebox.showinfo("Success", "Match score updated!", parent=self)
            self.on_success_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("API Error", f"Could not update score:\n{e}", parent=self)


class TournamentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Football Tournament Manager")
        self.geometry("1000x650")

        self.is_organizer = False
        self.teams_map = {}
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

    def setup_tournaments_tab(self):
        if self.is_organizer:
            top_bar = ttk.Frame(self.tab_tournaments)
            top_bar.pack(fill="x", pady=(0, 10))
            ttk.Button(top_bar, text="+ New Tournament", command=lambda: CreateTournamentForm(self, self.refresh_all)).pack(side="left")

        self.tree_tournaments = ttk.Treeview(self.tab_tournaments, columns=("ID", "Name", "Start", "End"), show="headings")
        for col, h in [("ID", "ID"), ("Name", "Tournament Name"), ("Start", "Start Date"), ("End", "End Date")]:
            self.tree_tournaments.heading(col, text=h)
            self.tree_tournaments.column(col, anchor="center")
        self.tree_tournaments.pack(fill="both", expand=True)

    def setup_teams_tab(self):
        if self.is_organizer:
            top_bar = ttk.Frame(self.tab_teams)
            top_bar.pack(fill="x", pady=(0, 10))
            ttk.Button(top_bar, text="+ Add Team", command=lambda: CreateTeamForm(self, self.refresh_all)).pack(side="left")

        self.tree_teams = ttk.Treeview(self.tab_teams, columns=("ID", "Name", "Coach"), show="headings")
        for col, h in [("ID", "ID"), ("Name", "Team Name"), ("Coach", "Coach / Manager")]:
            self.tree_teams.heading(col, text=h)
            self.tree_teams.column(col, anchor="center")
        self.tree_teams.pack(fill="both", expand=True)

    def setup_matches_tab(self):
        if self.is_organizer:
            top_bar = ttk.Frame(self.tab_matches)
            top_bar.pack(fill="x", pady=(0, 10))
            ttk.Button(top_bar, text="+ Schedule Match", command=lambda: ScheduleMatchForm(self, self.refresh_all)).pack(side="left", padx=(0, 5))
            ttk.Button(top_bar, text="⚽ Update Score", command=self.open_update_score).pack(side="left")

        self.tree_matches = ttk.Treeview(self.tab_matches, columns=("ID", "Date", "Home", "Score", "Away", "Referee"), show="headings")
        cols = [
            ("ID", "ID", 50),
            ("Date", "Match Date", 120),
            ("Home", "Home Team", 200),
            ("Score", "Score", 80),
            ("Away", "Away Team", 200),
            ("Referee", "Referee", 150)
        ]
        for col, h, w in cols:
            self.tree_matches.heading(col, text=h)
            self.tree_matches.column(col, anchor="center", width=w)
        self.tree_matches.pack(fill="both", expand=True)

    def open_update_score(self):
        selected = self.tree_matches.selection()
        if not selected:
            messagebox.showwarning("Select Match", "Please select a match from the table first!")
            return

        item = self.tree_matches.item(selected[0])
        vals = item['values']
        match_id = vals[0]
        home_team = vals[2]
        away_team = vals[4]

        UpdateScoreForm(self, match_id, home_team, away_team, self.refresh_all)

    def setup_standings_tab(self):
        self.tree_standings = ttk.Treeview(
            self.tab_standings, 
            columns=("Pos", "Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"), 
            show="headings"
        )
        cols = [
            ("Pos", "#", 40),
            ("Team", "Team Name", 220),
            ("P", "Played", 60),
            ("W", "Won", 60),
            ("D", "Drawn", 60),
            ("L", "Lost", 60),
            ("GF", "GF", 60),
            ("GA", "GA", 60),
            ("GD", "GD", 60),
            ("Pts", "Points", 80)
        ]
        for col, h, w in cols:
            self.tree_standings.heading(col, text=h)
            self.tree_standings.column(col, anchor="center", width=w)
        self.tree_standings.pack(fill="both", expand=True)

    def refresh_all(self):
        # Tournaments
        for item in self.tree_tournaments.get_children():
            self.tree_tournaments.delete(item)
        try:
            for t in api.get_tournaments():
                self.tree_tournaments.insert("", "end", values=(t.get("tournament_id"), t.get("name"), t.get("start_date"), t.get("end_date")))
        except Exception:
            pass

        # Teams
        for item in self.tree_teams.get_children():
            self.tree_teams.delete(item)
        self.teams_map = {}
        try:
            for item in api.get_teams():
                t_id = item.get("team_id")
                t_name = item.get("name")
                self.teams_map[t_id] = t_name
                coach = item.get("coach_name") or item.get("manager_name") or item.get("coach") or "N/A"
                self.tree_teams.insert("", "end", values=(t_id, t_name, coach))
        except Exception:
            pass

        # Matches & Standings calculation
        for item in self.tree_matches.get_children():
            self.tree_matches.delete(item)
        for item in self.tree_standings.get_children():
            self.tree_standings.delete(item)

        standings_data = {
            tid: {"name": name, "P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}
            for tid, name in self.teams_map.items()
        }

        try:
            for m in api.get_matches():
                home_id = m.get("home_team_id")
                away_id = m.get("away_team_id")
                home_name = self.teams_map.get(home_id, f"Team #{home_id}")
                away_name = self.teams_map.get(away_id, f"Team #{away_id}")
                referee = m.get("referee", "N/A")

                h_score = m.get("home_score")
                a_score = m.get("away_score")

                if h_score is not None and a_score is not None:
                    score_str = f"{h_score} - {a_score}"
                    
                    if home_id in standings_data and away_id in standings_data:
                        h_team = standings_data[home_id]
                        a_team = standings_data[away_id]

                        h_team["P"] += 1
                        a_team["P"] += 1
                        h_team["GF"] += h_score
                        h_team["GA"] += a_score
                        a_team["GF"] += a_score
                        a_team["GA"] += h_score

                        if h_score > a_score:
                            h_team["W"] += 1
                            h_team["Pts"] += 3
                            a_team["L"] += 1
                        elif a_score > h_score:
                            a_team["W"] += 1
                            a_team["Pts"] += 3
                            h_team["L"] += 1
                        else:
                            h_team["D"] += 1
                            a_team["D"] += 1
                            h_team["Pts"] += 1
                            a_team["Pts"] += 1
                else:
                    score_str = "-"

                self.tree_matches.insert("", "end", values=(m.get("match_id"), m.get("match_date"), home_name, score_str, away_name, referee))
        except Exception:
            pass

        sorted_standings = sorted(
            standings_data.values(),
            key=lambda x: (x["Pts"], x["GF"] - x["GA"], x["GF"]),
            reverse=True
        )

        for pos, st in enumerate(sorted_standings, start=1):
            gd = st["GF"] - st["GA"]
            self.tree_standings.insert("", "end", values=(
                pos, st["name"], st["P"], st["W"], st["D"], st["L"], st["GF"], st["GA"], gd, st["Pts"]
            ))


if __name__ == "__main__":
    app = TournamentApp()
    app.mainloop()
