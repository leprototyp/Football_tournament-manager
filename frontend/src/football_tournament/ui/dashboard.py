import tkinter as tk
from tkinter import ttk, messagebox
from football_tournament import api

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Football Tournament Manager")
        self.parent.geometry("900x650")
        
        self._build_ui()
        self._load_data()
    
    def _build_ui(self):
        main = tk.Frame(self.parent, padx=15, pady=15)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            header_frame, 
            text="🏆 Football Tournament Manager",
            font=("Arial", 18, "bold")
        ).pack(side=tk.LEFT)
        
        tk.Button(
            header_frame, 
            text="🔄 Refresh Data", 
            command=self._load_data,
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 10, "bold"),
            padx=12, 
            pady=4,
            bd=0,
            cursor="hand2"
        ).pack(side=tk.RIGHT)
        
        # Tabs Notebook
        notebook = ttk.Notebook(main)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 1. Tournaments Tab
        self.tournament_frame = tk.Frame(notebook)
        notebook.add(self.tournament_frame, text="🏟️ Tournaments")
        self._build_tournament_tab(self.tournament_frame)
        
        # 2. Standings / Ranking Tab
        self.ranking_frame = tk.Frame(notebook)
        notebook.add(self.ranking_frame, text="📊 Standings")
        self._build_ranking_tab(self.ranking_frame)
        
        # 3. Teams Tab
        self.teams_frame = tk.Frame(notebook)
        notebook.add(self.teams_frame, text="⚽ Teams")
        self._build_teams_tab(self.teams_frame)
        
        # 4. Matches Tab
        self.matches_frame = tk.Frame(notebook)
        notebook.add(self.matches_frame, text="📅 Matches")
        self._build_matches_tab(self.matches_frame)
    
    def _build_tournament_tab(self, parent):
        tk.Label(parent, text="Tournaments List", font=("Arial", 12, "bold")).pack(anchor="w", pady=10, padx=5)
        
        columns = ("ID", "Name", "Start Date", "End Date", "Organizer")
        self.tournaments_tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
        
        headings = ["ID", "Tournament Name", "Start Date", "End Date", "Organizer"]
        widths = [60, 220, 120, 120, 150]
        
        for col, head, w in zip(columns, headings, widths):
            self.tournaments_tree.heading(col, text=head)
            self.tournaments_tree.column(col, width=w, anchor="center" if "Date" in head or col == "ID" else "w")
        
        self.tournaments_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    def _build_ranking_tab(self, parent):
        frame_top = tk.Frame(parent)
        frame_top.pack(fill=tk.X, pady=10, padx=5)
        
        tk.Label(frame_top, text="Select Tournament:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.ranking_tournament_var = tk.StringVar()
        self.ranking_combo = ttk.Combobox(frame_top, textvariable=self.ranking_tournament_var, width=35, state="readonly")
        self.ranking_combo.pack(side=tk.LEFT)
        self.ranking_combo.bind("<<ComboboxSelected>>", self._load_ranking)
        
        columns = ("Position", "Team", "Played", "Points")
        self.ranking_tree = ttk.Treeview(parent, columns=columns, show="headings", height=12)
        
        self.ranking_tree.heading("Position", text="Pos")
        self.ranking_tree.heading("Team", text="Team Name")
        self.ranking_tree.heading("Played", text="Played")
        self.ranking_tree.heading("Points", text="Points")
        
        self.ranking_tree.column("Position", width=60, anchor="center")
        self.ranking_tree.column("Team", width=250, anchor="w")
        self.ranking_tree.column("Played", width=100, anchor="center")
        self.ranking_tree.column("Points", width=100, anchor="center")
        
        self.ranking_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    def _build_teams_tab(self, parent):
        tk.Label(parent, text="Registered Teams", font=("Arial", 12, "bold")).pack(anchor="w", pady=10, padx=5)
        
        columns = ("ID", "Name", "Coach")
        self.teams_tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
        
        self.teams_tree.heading("ID", text="ID")
        self.teams_tree.heading("Name", text="Team Name")
        self.teams_tree.heading("Coach", text="Head Coach")
        
        self.teams_tree.column("ID", width=60, anchor="center")
        self.teams_tree.column("Name", width=250, anchor="w")
        self.teams_tree.column("Coach", width=200, anchor="w")
        
        self.teams_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    def _build_matches_tab(self, parent):
        tk.Label(parent, text="Match Schedule & Results", font=("Arial", 12, "bold")).pack(anchor="w", pady=10, padx=5)
        
        columns = ("Date", "Home Team", "Score", "Away Team")
        self.matches_tree = ttk.Treeview(parent, columns=columns, show="headings", height=10)
        
        self.matches_tree.heading("Date", text="Match Date")
        self.matches_tree.heading("Home Team", text="Home Team")
        self.matches_tree.heading("Score", text="Score")
        self.matches_tree.heading("Away Team", text="Away Team")
        
        self.matches_tree.column("Date", width=130, anchor="center")
        self.matches_tree.column("Home Team", width=200, anchor="e")
        self.matches_tree.column("Score", width=100, anchor="center")
        self.matches_tree.column("Away Team", width=200, anchor="w")
        
        self.matches_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    def _load_data(self):
        try:
            tournaments = api.get_tournaments()
            self._update_tournaments(tournaments)
            
            teams = api.get_teams()
            self._update_teams(teams)
            
            matches = api.get_matches()
            self._update_matches(matches)
            
            self._update_ranking_combo(tournaments)
            
            if tournaments:
                self.ranking_combo.set(tournaments[0].get('name', ''))
                self._load_ranking()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def _update_tournaments(self, tournaments):
        for item in self.tournaments_tree.get_children():
            self.tournaments_tree.delete(item)
        
        for t in tournaments:
            self.tournaments_tree.insert("", tk.END, values=(
                t.get('tournament_id', ''),
                t.get('name', ''),
                t.get('start_date', ''),
                t.get('end_date', ''),
                t.get('organizer_name', 'N/A')
            ))
    
    def _update_teams(self, teams):
        for item in self.teams_tree.get_children():
            self.teams_tree.delete(item)
        
        for t in teams:
            self.teams_tree.insert("", tk.END, values=(
                t.get('team_id', ''),
                t.get('name', ''),
                t.get('coach', 'N/A')
            ))
    
    def _update_matches(self, matches):
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
        
        for m in matches:
            score = f"{m.get('home_score', 0)} - {m.get('away_score', 0)}"
            self.matches_tree.insert("", tk.END, values=(
                m.get('match_date', ''),
                m.get('home_team_name', ''),
                score,
                m.get('away_team_name', '')
            ))
    
    def _update_ranking_combo(self, tournaments):
        names = [t['name'] for t in tournaments if 'name' in t]
        self.ranking_combo['values'] = names
    
    def _load_ranking(self, event=None):
        try:
            selected = self.ranking_tournament_var.get()
            if not selected:
                return
            
            for item in self.ranking_tree.get_children():
                self.ranking_tree.delete(item)
            
            # S'assure de ne pas crasher si la méthode ranking n'est pas encore implémentée dans api.py
            if hasattr(api, "get_tournament_ranking"):
                tournaments = api.get_tournaments()
                tournament_id = next((t.get('tournament_id') for t in tournaments if t.get('name') == selected), None)
                
                if tournament_id:
                    ranking = api.get_tournament_ranking(tournament_id)
                    for i, row in enumerate(ranking, 1):
                        self.ranking_tree.insert("", tk.END, values=(
                            i,
                            row.get('team_name', ''),
                            row.get('matches_played', 0),
                            row.get('points', 0)
                        ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load standings: {e}")
