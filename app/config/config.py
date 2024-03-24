import os
import json

from fastapi import HTTPException
from fastapi.responses import JSONResponse

class DBConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Enviroment():

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self, value: str):
        if self._host == '' and value != '':
            self._host = value
    
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value: str):
        if self._user == '':
            self._user = value
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value: str):
        if self._password == '':
            self._password = value
    
    @property
    def database(self):
        return self._database
    
    @database.setter
    def database(self, value: str):
        if self._database == '':
            self._database = value

    @property
    def token_expiration_time(self):
        time = self._token_expiration_time
        if time == 0:
            time = 15
            self.token_expiration_time = 15
        return time
    
    @token_expiration_time.setter
    def token_expiration_time(self, value: int|float|complex) -> int|float|complex:
        if not isinstance(value, (int, float, complex)):
            raise AttributeError(f"token_expiration_tipe can't be an {type(value)}, expected value would be int, float or complex")
        self._token_expiration_time = value

    def db(self):
        import database.mysql as mysql
        import database.sqlite as sqlite 

        if self.connector == 'sqlite':
            self.DB = sqlite.DB
        elif self.connector == 'mysql':
            self.DB = mysql.DB
        else:
            raise DBConfigException(f'The setted connector{self.connector}, is not supported')


    def __init__(self) -> None:
        self.local = True
        self.debug = {
            "all": False,
            "items": {
                "errors": {
                    "description": "Error messages",
                    "validation": False,
                    "group": ""
                },
                "askForQueries": {
                    "description": "Asking confirmation to execute a querie",
                    "validation": False,
                    "group": ""
                },
                "queriesResponse": {
                    "description": "Response after an query execution",
                    "validation": False,
                    "group": ""
                },
                "eTimeDbCon": {
                    "description": "Elapsed time of a database connection",
                    "validation": False,
                    "group": "elapsedTimes"
                },
                "eTimeFunc": {
                    "description": "Elapsed time of a function",
                    "validation": True,
                    "group": "elapsedTimes"
                },
                "executedFunction": {
                    "description": "after query executions",
                    "validation": False,
                    "group": ""
                },
            },
            "groups": {
                "elapsedTimes": False,
                "confirmation": False,
            }
        }
        self._connector: str
        self._host: str = ''
        self._user: str = ''
        self._password: str = ''
        self._database: str = ''
        self._token_expiration_time = 0

        # read env file to set configuration
        with open("env.json", 'r', encoding="utf-8") as file:
            content = file.read()
            file.close()
        
        try:

            content:dict = json.loads(content)
            database_context:dict = content.get('database',{})
            
            self.connector = database_context.get("connector",'')

            self.host = database_context.get("host")
            self.user = database_context.get("user")
            self.password = database_context.get("password")
            self.database = database_context.get("schema")

            validator = self.host == '' or self.user == '' or self.password == '' or self.database == ''

            if validator:
                raise DBConfigException('Some Database configuration params is not configured.')

        except DBConfigException as e:
            # Try get params of os.environ
            # Only assign values to parameters of empty variables. If a parameter has already been set (whether one or more), it will not be updated.
            print(e)
            try:
                self.host = os.environ["host"]
                self.user = os.environ["user"]
                self.password = os.environ["password"]
                self.database = os.environ["database"]
                self.local = False
            except Exception as e:
                print(f'OS Environ key exception: {e}')
                exit()
    
    def confirmation(self,message:str,validator:str) -> bool:
        """
        For debugging purposes, this function prompts for confirmation before executing any given function. It's commonly used during the development process to confirm changes and prevent errors in critical actions.

        (not work on backend applications)

        Params
        -----
            message: string
                A message displayed to the user during runtime.
            validator: string
                Compares the user-provided prompt with the validator. If they are identical, it returns true.
        Returns
        -----
        boolean
            
        Exceptions
        -----
            This function does not throw an exception. If an error occurs during runtime, it returns a false value and prints the error.

        """
        try:
            if not self.debug["all"]:
                # Validación del grupo de confirmaciones
                if not self.debug["groups"]["confirmation"]:
                    # Validación del grupo de el item específico
                    if not self.debug["items"]["askForQueries"]["validation"]:
                        return True
            validation = input(message)
            return not validation == validator
        except Exception as e:
            self.print("Error occurred during the execution of the environment confirmation function.","errors")
            return False

    def print(self, message: str, type: str) -> None:
        """
         For debugging purposes, this function prompts for confirmation before executing any given function. It's commonly used during the development process to confirm changes and prevent errors in critical actions.

        (not work on backend applications)

        Params
        -----
            message:
                A message displayed to the user during runtime.
            type: string
                Find the type on environ configurations, it would be:
                    errors,
                    askForQueries,
                    queriesResponse,
                    eTimeDbCon,
                    eTimeFunc,
                    executedFunction
        Returns
        -----
        boolean
            
        Exceptions
        -----
            This function does not throw an exception. If an error occurs during runtime, it returns a false value and prints the error.
        
        """
        try:
            if not (self.debug["all"]):
                if not (self.debug["items"][type]["validation"]):
                    return
        except Exception as e:
            print(f"exception on environ print: {e}")
        print(message, end="\n")

    @staticmethod
    def response(
            message:str="",
            data:any=[],
            error:str="",
            statusCode:int=200,
            headers:dict={}
        ) -> JSONResponse:
        """
        This is utilized in backend applications to generate a standard response.

        Params
        -----

        Returns
        -----
        JSONResponse

        Exceptions
        -----
            No exceptions yet


        """
        response = JSONResponse( 
            status_code= statusCode,
            headers= {
                "Content-Type": "application/json",
                **headers
            },
            content = json.dumps({
                "message": message,
                "data": data,
                "error": error,
            })
        )

        return response
    
    @staticmethod
    def Exception(e: Exception) -> JSONResponse:
        print(f"handler exception {type(e)}")
        if type(e) == HTTPException:
            print("Print exception",e.status_code,e.detail)
            return JSONResponse(status_code=e.status_code,content=json.loads(e.detail))
        else:
            #print(e.with_traceback())
            return JSONResponse(status_code=500, content=e.args)
# Clase temporizador

environ = Enviroment()