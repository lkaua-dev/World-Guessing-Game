import tkinter as tk
from tkinter import messagebox
from .game import GameWindow
from .ranking import RankingWindow

class MainMenu(tk.Tk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.title("World Guessing Game")
        self.geometry("350x400")
        self.configure(bg="#2c3e50")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="🌎", font=("Arial", 50), bg="#2c3e50").pack(pady=(40, 10))
        tk.Label(self, text="WORLD GUESS", font=("Arial", 20, "bold"), fg="white", bg="#2c3e50").pack(pady=5)

        style_btn = {"font": ("Arial", 12), "width": 20, "pady": 5}

        tk.Button(self, text="🎮 Novo Jogo", command=self.open_game_setup, bg="#27ae60", fg="white", **style_btn).pack(pady=20)
        tk.Button(self, text="🏆 Ver Ranking", command=self.open_ranking, bg="#f39c12", fg="white", **style_btn).pack(pady=5)
        tk.Button(self, text="🚪 Sair", command=self.destroy, bg="#c0392b", fg="white", **style_btn).pack(pady=5)

    def open_game_setup(self):
        setup_window = tk.Toplevel(self)
        setup_window.title("Novo Jogo")
        setup_window.geometry("300x250")
        setup_window.configure(bg="#f0f0f0")

        tk.Label(setup_window, text="Nome do Jogador:", bg="#f0f0f0").pack(pady=(20, 5))
        entry_name = tk.Entry(setup_window, font=("Arial", 12))
        entry_name.pack(pady=5)
        entry_name.focus_set()

        def start_game(event=None):
            name = entry_name.get()
            if not name:
                messagebox.showwarning("Aviso", "Digite um nome para jogar!")
                return
            setup_window.destroy()
            GameWindow(self, self.db_manager, name)

        entry_name.bind("<Return>", start_game)
        tk.Button(setup_window, text="INICIAR AVENTURA", command=start_game, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

    def open_ranking(self):
        RankingWindow(self, self.db_manager)