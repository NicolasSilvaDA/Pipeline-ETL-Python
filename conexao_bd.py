"""
    Este módulo é responsável por estabelecer e gerenciar todas
    as operações referentes ao banco de dados   
"""

# MySQL <-> Python
import mysql.connector
from mysql.connector import Error
# import pandas as pd 

# Tratamento de senha
from getpass import getpass

class ConectorBD:

    # Conexão com o banco de dados
    def __init__(self) -> None:

        connection = None
        while True:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user=input("Usuário: "),
                    passwd=getpass("Senha: "),
                    database="bmi_data"
                )

                print("Conexão com o banco de dados bem-sucedida!")
                self.conexaoBD = connection
                break

            except Error as err:
                print(f'Erro: "{err}"')

    def executar_query(self, query):
        cursor = self.conexaoBD.cursor()

        try:
            cursor.execute(query)
            self.conexaoBD.commit()
            print("Query realizada com sucesso!")
        except Error as err:
            print(f'Erro: "{err}"')

    def executar_fetch(self, query):
        cursor = self.conexaoBD.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        
        except Error as err:
            print(f'Erro: "{err}"')

conexaoBD = ConectorBD()