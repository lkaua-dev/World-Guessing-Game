from database import DatabaseManager
from api import CountriesAPI
from views.menu import MainMenu

def main():
    # 1. Inicializa o Banco de Dados
    db = DatabaseManager()
    
    # 2. Verifica/Atualiza dados da API
    CountriesAPI.populate_database(db)
    
    # 3. Inicia a Interface Gráfica
    app = MainMenu(db)
    app.mainloop()

if __name__ == "__main__":
    main()