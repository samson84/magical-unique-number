from typing import Optional, List, Dict, Callable, Tuple, Any, Iterable
import psycopg2

database_instance=None

def connect_db(db_name: str, user: str, password: str, host: Optional[str] = 'localhost', port: Optional[str] = 5432):
    global database_instance
    database_instance = Database(db_name, user, password, host, port) 

def get_db():
    return database_instance

class Database():
    def __init__(self, db_name: str, user: str, password: str, host: Optional[str] = 'localhost', port: Optional[str] = 5432):
        self.connection = None
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_connection(self):
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port)
        return self.connection

    def query(self, query_string: str, params: Optional[Tuple[Any]]=None) -> Iterable[Tuple]:
        with self.get_connection().cursor() as cursor:
            cursor.execute(query_string, params)
            for record in cursor:
                yield record
        
    def close_connection(self):
        if self.connection is not None:
            self.connection.close()