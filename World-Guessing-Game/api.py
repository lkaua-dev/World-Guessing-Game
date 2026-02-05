import requests
from tkinter import messagebox

class CountriesAPI:
    @staticmethod
    def populate_database(db_manager):
        """Verifica se o banco está vazio e popula se necessário."""
        if not db_manager.is_empty():
            return

        try:
            print("Baixando e traduzindo dados...")
            url = "https://restcountries.com/v3.1/all?fields=name,capital,region,flags,translations"
            response = requests.get(url)
            dados = response.json()

            traducao_regioes = {
                "Africa": "África", "Americas": "Américas", "Asia": "Ásia",
                "Europe": "Europa", "Oceania": "Oceania", "Antarctic": "Antártida",
            }

            for pais in dados:
                try:
                    nome = pais["translations"]["por"]["common"]
                except KeyError: 
                    nome = pais["name"]["common"]

                capital = pais["capital"][0] if pais.get("capital") else "Sem Capital"
                regiao_en = pais.get("region", "Desconhecida")
                regiao = traducao_regioes.get(regiao_en, regiao_en)
                bandeira_url = pais.get("flags", {}).get("png", "")

                db_manager.add_country(nome, capital, regiao, bandeira_url)
            
            print("Banco de dados atualizado!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar dados da API: {e}")