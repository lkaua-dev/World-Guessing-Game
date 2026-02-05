import tkinter as tk
from tkinter import messagebox
import base64
import requests
from utils import normalizar_texto

class GameWindow(tk.Toplevel):
    def __init__(self, parent, db_manager, player_name):
        super().__init__(parent)
        self.db_manager = db_manager
        self.player_name = player_name
        self.attempts = 0
        self.max_attempts = 3
        
        # Busca dados do país: (nome, capital, regiao, url)
        self.country_data = self.db_manager.get_random_country()
        
        self.setup_ui()
        self.update_hint()

    def setup_ui(self):
        self.geometry("400x550")
        self.configure(bg="#f0f0f0")
        self.title(f"Jogando: {self.player_name}")

        tk.Label(self, text=f"👤 Jogador: {self.player_name}", font=("Arial", 10), bg="#f0f0f0").pack(pady=5)

        self.lbl_hint_title = tk.Label(self, text="DICA ATUAL:", fg="#0055ff", font=("Arial", 14, "bold"), bg="#f0f0f0")
        self.lbl_hint_title.pack(pady=10)

        self.lbl_hint_content = tk.Label(self, text="...", font=("Arial", 16), wraplength=350, bg="#f0f0f0")
        self.lbl_hint_content.pack(pady=10)

        self.frame_flag = tk.Frame(self, bg="#f0f0f0", height=150)
        self.frame_flag.pack(pady=5)
        self.lbl_flag = tk.Label(self.frame_flag, bg="#f0f0f0")
        self.lbl_flag.pack()

        tk.Label(self, text="Qual é o país?", bg="#f0f0f0").pack(pady=(20, 0))
        self.entry_answer = tk.Entry(self, font=("Arial", 14), justify="center")
        self.entry_answer.pack(pady=5)
        self.entry_answer.bind("<Return>", lambda event: self.check_answer())

        tk.Button(self, text="CONFIRMAR", command=self.check_answer, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20).pack(pady=15)

        self.lbl_status = tk.Label(self, text="Tentativa 1 de 3", fg="#666", bg="#f0f0f0")
        self.lbl_status.pack(pady=5)

    def update_hint(self):
        nome, capital, regiao, bandeira_url = self.country_data

        if self.attempts == 0:
            self.lbl_hint_title.config(text="🌎 DICA 1 - REGIÃO")
            self.lbl_hint_content.config(text=regiao)
        elif self.attempts == 1:
            self.lbl_hint_title.config(text="🏙️ DICA 2 - CAPITAL")
            self.lbl_hint_content.config(text=capital)
        elif self.attempts == 2:
            self.lbl_hint_title.config(text="🚩 DICA 3 - BANDEIRA")
            self.lbl_hint_content.config(text="Carregando imagem...")
            self.update() 
            self.load_flag_image(bandeira_url)

        self.lbl_status.config(text=f"Tentativa {self.attempts + 1} de 3")

    def load_flag_image(self, url):
        try:
            response = requests.get(url, timeout=5)
            img_data = base64.encodebytes(response.content)
            self.img_ref = tk.PhotoImage(data=img_data) 
            self.lbl_flag.config(image=self.img_ref)
            self.lbl_hint_content.config(text="")
        except:
            self.lbl_hint_content.config(text="[Erro ao carregar imagem]")

    def check_answer(self):
        guess = normalizar_texto(self.entry_answer.get())
        correct = normalizar_texto(self.country_data[0])

        if guess == correct:
            self.handle_win()
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.handle_game_over()
            else:
                messagebox.showwarning("Incorreto", "Resposta errada! Veja a próxima dica.")
                self.entry_answer.delete(0, tk.END)
                self.update_hint()

    def handle_win(self):
        points = [100, 50, 25][self.attempts]
        self.db_manager.save_score(self.player_name, points)
        messagebox.showinfo("PARABÉNS!", f"Você acertou! \n\nO país era: {self.country_data[0]}\nPontos ganhos: {points}")
        self.destroy()

    def handle_game_over(self):
        messagebox.showerror("GAME OVER", f"Que pena, suas chances acabaram.\n\nO país era: {self.country_data[0]}")
        self.destroy()