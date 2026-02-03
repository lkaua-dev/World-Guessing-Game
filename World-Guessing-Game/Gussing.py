# --- Bibliotecas utilizadas ---

import tkinter as tk
from tkinter import messagebox


def janela_Main():
    janelamain = tk.Toplevel()
    janelamain.title("Main")
    janelamain.geometry("300x300")

    label_nome = tk.Label(janelamain, text="Nome do Jogador:")
    label_nome.pack(pady=10)

    campo_nome = tk.Entry(janelamain)
    campo_nome.pack(pady=10)

    botao_salvar = tk.Button(
        janelamain,
        text="Iniciar",
        command=lambda: messagebox.showinfo(
            "Info", f"Filme: {campo_nome.get()}"
        )
    )
    botao_salvar.pack(pady=20)


tela_principal = tk.Tk()
tela_principal.title("World Guessing Game")
tela_principal.geometry("300x300")

botao_New_Game = tk.Button(
    tela_principal,
    text="New Game",
    command=janela_Main
)
botao_New_Game.pack(pady=10)

botao_Ranking = tk.Button(
    tela_principal,
    text="Ranking",
    command=janela_Main
)
botao_Ranking.pack(pady=10)

botao_Sair = tk.Button(
    tela_principal,
    text="Sair",
    command=janela_Main
)
botao_Sair.pack(pady=10)

tela_principal.mainloop()
