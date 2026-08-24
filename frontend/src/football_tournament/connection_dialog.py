import tkinter as tk
from tkinter import messagebox

class ConnectionDialog:
    def __init__(self, parent):
        self.parent = parent
        self.confirmed = False
        self.url = "http://localhost:8000"
        self.token = ""
        
        self._build_ui()
        self.window.wait_window()
    
    def _build_ui(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Connexion à l'API")
        self.window.geometry("450x220")
        self.window.resizable(False, False)
        self.window.grab_set()
        self.window.transient(self.parent)
        
        # Forcer l'affichage
        self.window.lift()
        self.window.focus_force()
        self.window.update()
        
        self.url_var = tk.StringVar(value="http://localhost:8000")
        self.token_var = tk.StringVar()
        
        main = tk.Frame(self.window, padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main, text="URL de l'API:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        tk.Entry(main, textvariable=self.url_var, width=40).grid(
            row=1, column=0, pady=(0, 15))
        
        tk.Label(main, text="X-API-Token:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        tk.Entry(main, textvariable=self.token_var, width=40, show="*").grid(
            row=3, column=0, pady=(0, 15))
        
        button_frame = tk.Frame(main)
        button_frame.grid(row=4, column=0, pady=10)
        
        tk.Button(button_frame, text="Se connecter", command=self._confirm,
                  bg="#4CAF50", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Annuler", command=self._cancel,
                  bg="#f44336", fg="white", padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        self.window.protocol("WM_DELETE_WINDOW", self._cancel)
        
        # Forcer le rafraîchissement
        self.window.update()
    
    def _confirm(self):
        url = self.url_var.get().strip()
        token = self.token_var.get().strip()
        
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL d'API")
            return
        
        if not url.startswith(("http://", "https://")):
            messagebox.showerror("Erreur", "L'URL doit commencer par http:// ou https://")
            return
        
        self.url = url.rstrip('/')
        self.token = token
        self.confirmed = True
        self.window.destroy()
    
    def _cancel(self):
        self.window.destroy()
