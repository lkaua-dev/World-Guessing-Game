import tkinter as tk

class RankingWindow(tk.Toplevel):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.title("Ranking Global")
        self.geometry("350x450")
        self.configure(bg="white")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="🏆 TOP 5 JOGADORES", font=("Arial", 16, "bold"), bg="white", fg="#FFD700").pack(pady=20)

        ranking_data = self.db_manager.get_top_ranking()

        if not ranking_data:
            tk.Label(self, text="Nenhum registro ainda.\nSeja o primeiro!", bg="white").pack()
            return

        for idx, (nome, ponto) in enumerate(ranking_data, 1):
            bg_color = "#f9f9f9" if idx % 2 == 0 else "white"
            frame = tk.Frame(self, bg=bg_color, pady=5)
            frame.pack(fill="x", padx=20)

            tk.Label(frame, text=f"{idx}º", font=("Arial", 12, "bold"), width=3, bg=bg_color).pack(side="left")
            tk.Label(frame, text=f"{nome}", font=("Arial", 12), width=15, anchor="w", bg=bg_color).pack(side="left")
            tk.Label(frame, text=f"{ponto} pts", font=("Arial", 12, "bold"), fg="#4CAF50", bg=bg_color).pack(side="right")