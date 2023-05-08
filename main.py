import getpass as gp
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template


def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect\
        (
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


db_name = "testeGitHub"
password = gp.getpass("Digite sua senha: ")

create_testeGitHub_database = f"CREATE DATABASE {db_name}"
create_cpf_table = """
CREATE TABLE cpf 
(
  id INT PRIMARY KEY,
  cpf VARCHAR(15) NOT NULL
);
 """
blacklist = open("blacklist.txt")
blacklist = blacklist.readlines()
connection = create_server_connection("localhost", "root", password, db_name)
execute_query(connection, create_cpf_table)

for i, valor in enumerate(blacklist):
    cpf = valor.strip()
    insert_item = f"INSERT INTO cpf VALUES({i+1}, '{cpf}');"
    execute_query(connection, insert_item)
    print(f"CPF: {valor} adicionado.")

is_saved = False
cpf_input = ""
while not cpf_input == "s":
    cpf_input = input("Pesquise um CPF: ")

    if cpf_input == "s":
        print("Encerrando...")
        break

    for valor in blacklist:
        cpf = valor.strip()

        if cpf == cpf_input:
            is_saved = True
            break
        else:
            is_saved = False

    if cpf_input == "":
        print("Running")

    if is_saved:
        print("Block")
    else:
        print("Free")
