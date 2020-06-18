from flask import Blueprint

rounds = Blueprint('rounds', __name__, url_prefix='rounds')

@rounds.route('/', methods=['GET'])
def get_rounds():
    return 'Hello World'
