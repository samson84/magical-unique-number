from typing import NamedTuple, Optional
from os import environ

from flask import Flask


from unique_number.routes.rounds import rounds
from unique_number.database.db import connect_db

class Config(NamedTuple):
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str


def create_app(test_config: Optional[Config] = None) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.register_blueprint(rounds, url_prefix='/rounds')
    if test_config is None:
        app.config.from_object(read_config_from_environment())
    else:
        app.config.from_object(test_config)

    connect_db(
        db_name=app.config['DB_NAME'],
        user = app.config['DB_USER'], 
        password=app.config['DB_PASSWORD']
    )
    return app

def read_config_from_environment() -> Config:
    return Config(
        DB_PASSWORD=environ.get('POSTGRES_PASSWORD'),
        DB_USER=environ.get('POSTGRES_USER'),
        DB_NAME=environ.get('POSTGRES_DB')
    )