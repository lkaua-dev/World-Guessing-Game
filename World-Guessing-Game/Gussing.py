# --- Bibliotecas utilizadas ---
import math
import datetime
import sqlite3 as sql
import requests
import tkinter as tk
from tkinter import messagebox
import unicodedata
import base64
import os

### --- CLASSE DO BANCO DE DADOS ---
class banco_dados:
    def setup_database(self):
        if os.path.exists("paises_game.db"):
            try:
                conn_check = sql.connect("paises_game.db")
                cursor_check = conn_check.cursor()
                cursor_check.execute("SELECT nome FROM paises LIMIT 1")
                conn_check.close()
            except:
                os.remove("paises_game.db")

        conn = sql.connect("paises_game.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS paises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                capital TEXT,
                regiao TEXT,
                bandeira_url TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jogador TEXT,
                pontos INTEGER
            )
        """
        )
        conn.commit()
        return conn, cursor

### --- CLASSE DA API ---
class api:
    @staticmethod
    def api_jogo(conn, cursor):
        cursor.execute("SELECT COUNT(*) FROM paises")
        if cursor.fetchone()[0] == 0:
            try:
                print("Baixando e traduzindo dados...")
                url = "https://restcountries.com/v3.1/all?fields=name,capital,region,flags,translations"
                response = requests.get(url)
                dados = response.json()

                traducao_regioes = {
                    "Africa": "África",
                    "Americas": "Américas",
                    "Asia": "Ásia",
                    "Europe": "Europa",
                    "Oceania": "Oceania",
                    "Antarctic": "Antártida",
                }

                for pais in dados:
                    try:
                        nome = pais["translations"]["por"]["common"]
                    except:
                        nome = pais["name"]["common"]

                    capital = (
                        pais["capital"][0] if pais.get("capital") else "Sem Capital"
                    )
                    regiao_en = pais.get("region", "Desconhecida")
                    regiao = traducao_regioes.get(regiao_en, regiao_en)
                    bandeira_url = pais.get("flags", {}).get("png", "")

                    cursor.execute(
                        "INSERT INTO paises (nome, capital, regiao, bandeira_url) VALUES (?, ?, ?, ?)",
                        (nome, capital, regiao, bandeira_url),
                    )
                conn.commit()
                print("Banco de dados atualizado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao baixar dados: {e}")

def normalizar_texto(texto):
    if not texto:
        return ""
    return (
        "".join(
            c
            for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
        .lower()
        .strip()
    )

### --- CLASSE DO JOGO ---
class Jogo:
    def __init__(self, janela, jogador):
        self.janela = janela
        self.jogador = jogador
        self.tentativas = 0
        self.max_tentativas = 3

        self.conn = sql.connect("paises_game.db")
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT nome, capital, regiao, bandeira_url FROM paises ORDER BY RANDOM() LIMIT 1"
        )
        self.dados_pais = cursor.fetchone()
        self.conn.close()

        self.construir_interface_jogo()
        self.atualizar_dica()

    def construir_interface_jogo(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.janela.geometry("400x550")
        self.janela.configure(bg="#f0f0f0")

        tk.Label(
            self.janela,
            text=f"👤 Jogador: {self.jogador}",
            font=("Arial", 10),
            bg="#f0f0f0",
        ).pack(pady=5)

        self.lbl_dica_titulo = tk.Label(
            self.janela,
            text="DICA ATUAL:",
            fg="#0055ff",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
        )
        self.lbl_dica_titulo.pack(pady=10)

        self.lbl_dica_conteudo = tk.Label(
            self.janela, text="...", font=("Arial", 16), wraplength=350, bg="#f0f0f0"
        )
        self.lbl_dica_conteudo.pack(pady=10)

        self.frame_bandeira = tk.Frame(self.janela, bg="#f0f0f0", height=150)
        self.frame_bandeira.pack(pady=5)
        self.lbl_bandeira = tk.Label(self.frame_bandeira, bg="#f0f0f0")
        self.lbl_bandeira.pack()

        tk.Label(self.janela, text="Qual é o país?", bg="#f0f0f0").pack(pady=(20, 0))
        self.entry_resposta = tk.Entry(
            self.janela, font=("Arial", 14), justify="center"
        )
        self.entry_resposta.pack(pady=5)
        self.entry_resposta.bind("<Return>", lambda event: self.verificar_resposta())

        self.btn_chutar = tk.Button(
            self.janela,
            text="CONFIRMAR",
            command=self.verificar_resposta,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
        )
        self.btn_chutar.pack(pady=15)

        self.lbl_status = tk.Label(
            self.janela, text=f"Tentativa 1 de 3", fg="#666", bg="#f0f0f0"
        )
        self.lbl_status.pack(pady=5)

    def atualizar_dica(self):
        regiao, capital, bandeira_url = (
            self.dados_pais[2],
            self.dados_pais[1],
            self.dados_pais[3],
        )

        if self.tentativas == 0:
            self.lbl_dica_titulo.config(text="🌎 DICA 1 - REGIÃO")
            self.lbl_dica_conteudo.config(text=regiao)
        elif self.tentativas == 1:
            self.lbl_dica_titulo.config(text="🏙️ DICA 2 - CAPITAL")
            self.lbl_dica_conteudo.config(text=capital)
        elif self.tentativas == 2:
            self.lbl_dica_titulo.config(text="🚩 DICA 3 - BANDEIRA")
            self.lbl_dica_conteudo.config(text="Carregando imagem...")
            self.janela.update()
            try:
                response = requests.get(bandeira_url)
                img_data = base64.encodebytes(response.content)
                self.img_ref = tk.PhotoImage(data=img_data)
                self.lbl_bandeira.config(image=self.img_ref)
                self.lbl_dica_conteudo.config(text="")
            except:
                self.lbl_dica_conteudo.config(
                    text="[Erro ao carregar imagem]\nMas não desista!"
                )

        self.lbl_status.config(text=f"Tentativa {self.tentativas + 1} de 3")

    def verificar_resposta(self):
        chute = normalizar_texto(self.entry_resposta.get())
        correto = normalizar_texto(self.dados_pais[0])

        if chute == correto:
            self.vitoria()
        else:
            self.tentativas += 1
            if self.tentativas >= self.max_tentativas:
                self.game_over()
            else:
                messagebox.showwarning(
                    "Incorreto", "Resposta errada! Veja a próxima dica."
                )
                self.entry_resposta.delete(0, tk.END)
                self.atualizar_dica()

    def vitoria(self):
        conn = sql.connect("paises_game.db")
        cursor = conn.cursor()
        pontos = [100, 50, 25][self.tentativas]
        cursor.execute(
            "INSERT INTO ranking (jogador, pontos) VALUES (?, ?)",
            (self.jogador, pontos),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo(
            "PARABÉNS!",
            f"Você acertou! \n\nO país era: {self.dados_pais[0]}\nPontos ganhos: {pontos}",
        )
        self.janela.destroy()

    def game_over(self):
        messagebox.showerror(
            "GAME OVER",
            f"Que pena, suas chances acabaram.\n\nO país era: {self.dados_pais[0]}",
        )
        self.janela.destroy()

def janela_Main():
    janelamain = tk.Toplevel()
    janelamain.title("Novo Jogo")
    janelamain.geometry("300x250")
    janelamain.configure(bg="#f0f0f0")

    tk.Label(janelamain, text="Nome do Jogador:", bg="#f0f0f0").pack(pady=(20, 5))
    campo_nome = tk.Entry(janelamain, font=("Arial", 12))
    campo_nome.pack(pady=5)
    campo_nome.focus_set()

    def iniciar(event=None):
        nome = campo_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Digite um nome para jogar!")
            return
        Jogo(janelamain, nome)

    campo_nome.bind("<Return>", iniciar)

    tk.Button(
        janelamain,
        text="INICIAR AVENTURA",
        command=iniciar,
        bg="#2196F3",
        fg="white",
        font=("Arial", 10, "bold"),
        pady=5,
    ).pack(pady=20)

def janela_ranking():
    janelaranking = tk.Toplevel()
    janelaranking.title("Ranking Global")
    janelaranking.geometry("350x450")
    janelaranking.configure(bg="white")

    tk.Label(
        janelaranking,
        text="🏆 TOP 5 JOGADORES",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#FFD700",
    ).pack(pady=20)

    conn = sql.connect("paises_game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT jogador, pontos FROM ranking ORDER BY pontos DESC LIMIT 5")
    ranking = cursor.fetchall()
    conn.close()

    if not ranking:
        tk.Label(
            janelaranking, text="Nenhum registro ainda.\nSeja o primeiro!", bg="white"
        ).pack()

    for idx, (nome, ponto) in enumerate(ranking, 1):
        bg_color = "#f9f9f9" if idx % 2 == 0 else "white"
        frame = tk.Frame(janelaranking, bg=bg_color, pady=5)
        frame.pack(fill="x", padx=20)

        tk.Label(
            frame, text=f"{idx}º", font=("Arial", 12, "bold"), width=3, bg=bg_color
        ).pack(side="left")
        tk.Label(
            frame, text=f"{nome}", font=("Arial", 12), width=15, anchor="w", bg=bg_color
        ).pack(side="left")
        tk.Label(
            frame,
            text=f"{ponto} pts",
            font=("Arial", 12, "bold"),
            fg="#4CAF50",
            bg=bg_color,
        ).pack(side="right")

# --- Início do Programa ---
db = banco_dados()
conexao, cursor_db = db.setup_database()
api.api_jogo(conexao, cursor_db)
conexao.close() # Fecha a conexão inicial após popular

if __name__ == "__main__":
    tela_principal = tk.Tk()
    tela_principal.title("World Guessing Game")
    tela_principal.geometry("350x400")
    tela_principal.configure(bg="#2c3e50")

    tk.Label(tela_principal, text="🌎", font=("Arial", 50), bg="#2c3e50").pack(
        pady=(40, 10)
    )
    tk.Label(
        tela_principal,
        text="WORLD GUESS",
        font=("Arial", 20, "bold"),
        fg="white",
        bg="#2c3e50",
    ).pack(pady=5)

    estilo_botao = {"font": ("Arial", 12), "width": 20, "pady": 5}

    tk.Button(
        tela_principal,
        text="🎮 Novo Jogo",
        command=janela_Main,
        bg="#27ae60",
        fg="white",
        **estilo_botao,
    ).pack(pady=20)
    tk.Button(
        tela_principal,
        text="🏆 Ver Ranking",
        command=janela_ranking,
        bg="#f39c12",
        fg="white",
        **estilo_botao,
    ).pack(pady=5)
    tk.Button(
        tela_principal,
        text="🚪 Sair",
        command=tela_principal.destroy,
        bg="#c0392b",
        fg="white",
        **estilo_botao,
    ).pack(pady=5)

    tela_principal.mainloop()
