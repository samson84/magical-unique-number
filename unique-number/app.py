from flask import Flask

from magical_unique_number.routes.rounds import rounds

def create_app(test_config = None):
    app = Flask(__name__)
    app.register_blueprint(rounds)
    return app