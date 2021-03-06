from typing import NamedTuple, Optional, Callable, List, Tuple
from contextlib import contextmanager
import random
import string

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import datetime

import config

from unique_number import create_app
from unique_number.utils.db_helpers import get_postgres_dsn

class MatchString():
    def __init__(self, matcher: Optional[str] = None):
        self.matcher=matcher
    def __eq__(self, other):
        if not isinstance(other, str):
            return False
        if isinstance(self.matcher, str):
            return self.matcher in other
        return True



@contextmanager
def app_test_context(test_data):
    db_name = generate_db_name('un_test')
    admin_dsn = get_postgres_dsn(
        password=config.TEST_DB_PASSWORD, 
        host=config.TEST_DB_HOST, 
        port=config.TEST_DB_PORT,         
        user=config.TEST_DB_USER,
        db_name=config.TEST_DB_BASE_DB_NAME
    )
    with prepared_db(dsn=admin_dsn, password=config.TEST_DB_PASSWORD, db_name=db_name, query=test_data, init_script=config.INIT_SCRIPT, keep_db=config.KEEP_DB):
        class AppConfig():
            DB_USER=config.TEST_DB_USER
            DB_PASSWORD=config.TEST_DB_PASSWORD
            DB_PORT=config.TEST_DB_PORT
            DB_HOST=config.TEST_DB_HOST
            DB_DB=db_name
    
        with app_test_client(create_app, AppConfig) as client:
            yield client

def create_vote_queries(votes: List[Tuple]) -> str:
    queries = []
    for vote in votes:
        (id, round_id, vote, username) = vote
        if id is None:
            query = f"INSERT INTO votes (round_id,vote,username) VALUES ({round_id}, {vote}, '{username}');"
        else:
            query = f"INSERT INTO votes (id,round_id,vote,username) VALUES ({id}, {round_id}, {vote}, '{username}');"
        queries.append(query)
    return '\n'.join(queries)

def create_round_queries(rounds: List[Tuple]) -> str:
    queries = []
    for round in rounds:
        (id, started_at, finished_at) = round
        finished_at = f"'{finished_at}'" if finished_at is not None else 'NULL'
        if id is None:
            query = f"INSERT INTO rounds (started_at,finished_at) VALUES ('{started_at}', {finished_at});"
        else:
            query = f"INSERT INTO rounds (id,started_at,finished_at) VALUES ({id}, '{started_at}', {finished_at});"
        queries.append(query)
    return '\n'.join(queries)

def generate_random_string(length: int) -> str:
    chars = string.ascii_lowercase + string.digits
    randomized = [random.choice(chars) for _ in range(length)]
    return ''.join(randomized)

def generate_db_name(prefix: str) -> str:
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    random_string = generate_random_string(10)
    return f'{prefix}_{timestamp}_{random_string}'        

@contextmanager
def app_test_client(factory: Callable, config: object):
    app = factory(test_config=config)
    app.testing = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@contextmanager
def prepared_db(dsn: str, password: str, db_name: str, query: str, init_script: str, keep_db: Optional[bool]=False):
    default_connection = connect(dsn)
    default_dsn_params = default_connection.get_dsn_parameters()
    default_dsn_params = {
        **default_dsn_params, 
        **{
            'password': password
        }
    }

    test_db_dsn_params = {
        **default_dsn_params, 
        **{
            'dbname': db_name,
            'password': password
        }
    }

    try: 
        default_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        default_cursor = default_connection.cursor()
        default_cursor.execute(f'CREATE DATABASE {db_name}')
        default_cursor.close()
        default_connection.close()

        connection = connect(**test_db_dsn_params)

        with open(init_script, 'r') as init_file:
            init_file_content = '\n'.join(init_file.readlines())

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(init_file_content)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
        connection.close()

        yield 
    finally:
        default_cursor.close()
        default_connection.close()
        if not keep_db:
            deleter_connection = connect(**default_dsn_params)
            deleter_connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = deleter_connection.cursor()
            cursor.execute(f'DROP DATABASE {db_name}')
            cursor.close()
            deleter_connection.close()
        default_connection.close()





