import sys
import os

# Dynamic path resolution for src folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from football_tournament.ui.dashboard import Dashboard
from football_tournament import api

def center_window(window, width, height):
    """Centers the application window on the screen."""
    window.update_idletasks()
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def force_focus(window):
    """Forces the Tkinter window to the foreground."""
    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)
    window.focus_force()

def run_app():
    print("🚀 Starting Application...")
    root = tk.Tk()
    root.title("Football Tournament Management System")
    root.configure(bg="#f0f2f5")

    main_w, main_h = 900, 650
    center_window(root, main_w, main_h)
    force_focus(root)

    # Container to keep the Connection Card centered
    center_container = tk.Frame(root, bg="#f0f2f5")
    center_container.place(relx=0.5, rely=0.5, anchor="center")

    # Connection Dialog Card (Ref: Proposal Figure 2)
    card = tk.Frame(
        center_container, 
        bg="white", 
        bd=1, 
        relief="solid", 
        padx=35, 
        pady=30
    )
    card.pack()

    tk.Label(
        card, 
        text="Football Tournament Management", 
        font=("Arial", 16, "bold"), 
        bg="white", 
        fg="#1a1a1a"
    ).pack(pady=(0, 5))

    tk.Label(
        card, 
        text="Enter backend API address and authentication key", 
        font=("Arial", 9), 
        bg="white", 
        fg="#666666"
    ).pack(pady=(0, 20))

    form_frame = tk.Frame(card, bg="white")
    form_frame.pack(fill="x")

    # API URL Field
    tk.Label(
        form_frame, 
        text="API URL", 
        font=("Arial", 10, "bold"), 
        bg="white", 
        anchor="w"
    ).pack(fill="x", pady=(5, 2))
    
    url_entry = tk.Entry(
        form_frame, 
        font=("Arial", 10), 
        bd=1, 
        relief="solid",
        width=35
    )
    url_entry.pack(fill="x", ipady=4, pady=(0, 12))
    url_entry.insert(0, "http://localhost:8000")

    # X-API-Key Field
    tk.Label(
        form_frame, 
        text="X-API-Key (Organizer Key)", 
        font=("Arial", 10, "bold"), 
        bg="white", 
        anchor="w"
    ).pack(fill="x", pady=(5, 2))
    
    key_entry = tk.Entry(
        form_frame, 
        font=("Arial", 10), 
        bd=1, 
        relief="solid",
        show="*"
    )
    key_entry.pack(fill="x", ipady=4, pady=(0, 15))

    def on_connect():
        api_url = url_entry.get().strip()
        api_key = key_entry.get().strip()

        if not api_url:
            messagebox.showwarning("Warning", "Please provide a valid API URL.")
            return

        # Configure client with provided URL and Key
        api.set_config(api_url, api_key)

        # Test connection
        try:
            api.check_health()
            print("📡 Connection established successfully!")
        except Exception as e:
            messagebox.showerror(
                "Connection Failed", 
                f"Could not connect to FastAPI Backend at {api_url}:\n\n{e}"
            )
            return

        # Destroy Connection Dialog and launch Dashboard
        center_container.destroy()
        Dashboard(root)

    btn_connect = tk.Button(
        card, 
        text="[ CONNECT ]", 
        command=on_connect, 
        bg="#2196F3", 
        fg="white", 
        font=("Arial", 11, "bold"),
        bd=0,
        cursor="hand2",
        pady=8
    )
    btn_connect.pack(fill="x", pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    run_app()
