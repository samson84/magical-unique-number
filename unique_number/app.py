from typing import NamedTuple, Optional
from os import environ

from flask import Flask, Response
import logging 
import traceback

from unique_number.routes.rounds import rounds_blueprint
from unique_number.database.db import connect_db
from unique_number.utils.errors import ApplicationError
from unique_number.utils.responses import create_error

logger = logging.getLogger('app')

class Config(NamedTuple):
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str

def handle_error(error: Exception) -> Response:
    if isinstance(error, ApplicationError):
        return create_error(
            message=error.message,
            error_code=error.error_code,
            status_code=error.status_code)

    traceback.print_exc()
    return create_error(
        message='Something really went wrong.',
        error_code='internal_server_error',
        status_code=500
    )

def create_app(test_config: Optional[Config] = None) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.register_error_handler(Exception, handle_error)

    app.register_blueprint(rounds_blueprint, url_prefix='/rounds')

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