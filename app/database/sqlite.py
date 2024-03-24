import datetime
import sqlite3
from .connector import dbConnector

class DB(dbConnector):
    conn = None
    cursor = None

    def __init__(self) -> None:
        self.connected = False
        self.connect()
        self.close()
        pass
    # Conectar a la base de datos SQLite (o crearla si no existe)

    def connect(self):
        if not self.connected:
            try:
                self.conn = sqlite3.connect('../sqlite_master.db')
                self.cursor = self.conn.cursor()
                self.connected = True
                print(f'connected on sqlite {self.connected}')
            except Exception as e:
                print(f"An error ocurred during database connection {e}")
                exit()
        
    def close(self):
        if self.connected:
            self.conn.close()
            self.connected = False

    def __exit__(self):
        self.close()

    def query(self,query,params=None,persist = False) -> list:
        self.connect()
        if params:
            self.cursor.executemany(query,params)
        else:
            self.cursor.execute(query)
        res = self.cursor.fetchall()
        if not persist:
            self.close()
        return res

    def first(self,query):
        return

    def insert(self) -> int:
        id: int = 0
        return id

    