import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()


class MySQLConnection:

    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        try:
            with self.connection.cursor() as cursor:
                print(f"Ejecutando consulta: {query}")
                cursor.execute(query, data)

                if cursor.description is not None:
                    return cursor.fetchall()

                if query.strip().lower().startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount

        except pymysql.MySQLError as e:
            print(f"Error en la base de datos: {e}")
            return False

        finally:
            self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)


def connect_to_mysql(db):
    return MySQLConnection(db)
