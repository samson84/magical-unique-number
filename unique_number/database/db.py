from typing import Optional, List, Dict, Callable, Tuple, Any, Iterable
from flask import g, current_app
import psycopg2
    
def get_db():
    if 'db' not in g:
        g.db = Database(current_app.config['DB_CONNECTION_STRING'])
    return g.db

def teardown_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close_connection

class Database():
    def __init__(self, connection_string: str):
        self.connection = None
        self.connection_string = connection_string

    def get_connection(self):
        if self.connection is None:
            self.connection = psycopg2.connect(self.connection_string)
        return self.connection

    def query(self, query_string: str, params: Optional[Tuple[Any]]=None) -> Iterable[Tuple]:
        connection = self.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query_string, params)
            connection.commit()
            for record in cursor:
                yield record
        
    def close_connection(self):
        if self.connection is not None:
            self.connection.close()