import pymysql as mysql
import sys, traceback

from config.config import environ
from .connector import dbConnector

class DB(dbConnector):
    connected = None
    conexion = None
    cur = None
    status = None
    error = None

    def __init__(self):
        self.connected = False
        self.connect()
        self.close()

    def connect(self):
        try:
            self.conexion = mysql.connect(
                host=environ.host,
                user=environ.user,
                passwd=environ.password,
                database=environ.database)
            self.cur = self.conexion.cursor()
            self.status = True
            self.connected = True
        except Exception as e:
            print(f"Ha ocurrido un error al intentar realizar la conexión {e.args}")
            exit()
            

    def close(self):
        # self.restoreCur()
        self.conexion.close()
        self.connected = False
        environ.print("Conexión finalizada","executedFunction")

    def restoreCur(self) -> None:
        self.cur.close()
        self.cur = self.conexion.cursor()
        environ.print("Cursor reestablecido","executedFunction")
    
    def commit(self)->bool:
        try:
            self.conexion.commit()
            self.close()
            environ.print(f"filas afectadas: {self.cur.rowcount}","queriesResponse")
            return True
        except Exception as e:
            print(f"error:{e}")
            return False

    def query(
            self,
            sql: str,
            args: tuple = None,
            persist: bool = False
        ):
        """
    Descripción breve de la función.

    Parameters
    ----------
    param1 : Tipo
        Descripción de param1.
    param2 : Tipo
        Descripción de param2.

    Returns
    -------
    Tipo
        Descripción de lo que retorna.

    Raises
    ------
    ExcepcionTipo
        Circunstancias en las que se lanza esta excepción.
    """
        message = f"""
Inicializando query:
    {sql}
Argumentos:
    {args}
"""
        #if not environ.confirmation(message+"ingresa x para cancelar o cualquier otra para continuar: ","x"):
        #    print("Ejecución cancelada\n\n")
        #    return False
        if (persist and not self.connected) or not persist:
            self.connect()
        try:
            self.cur.execute(sql, args)
        except Exception as e:
            self.error = e
            print(f'Existe un error en la consulta, mensaje de error: \n{e}\n\nquery:\n{message}',"errors")
            return False
        try:
            validation = (sql.find("INSERT") != -1) or (sql.find("UPDATE") != -1) or (sql.find("DELETE") != -1)
            if sql.find("SELECT") != -1 and not validation:
                self.res = self.cur.fetchall()
                self.titles = [i[0] for i in self.cur.description]
            if validation:   
                if not persist:
                    self.res = self.commit()
                else:
                    return True
            else:
                self.close()
            return self.res
        except Exception as e:
            self.error = e
            print(f"Hubo un error en el procesamiento del query {message}\n\nerror:{e}")
            exc_type, exc_value, exc_traceback = sys.exc_info()  # Obtiene la información de la excepción
            error_info = traceback.format_exception(exc_type, exc_value, exc_traceback)  # Formatea la información del error

            # Imprime la información del error
            for line in error_info:
                print(line)
            return False

    def first(self,query):
        return 

    def insert(self,query) -> int:
        id: int = 0
        return id