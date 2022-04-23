import psycopg2
from psycopg2 import *


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def getCursor():
    connection = create_connection("Infrastructure", "postgres", "2001", "localhost", "5432")
    return connection.cursor()

def getConnect():
    return create_connection("Infrastructure", "postgres", "2001", "localhost", "5432")

def closeConnect(connect, cursor):
    connect.close()
    cursor.close()


