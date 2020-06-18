from flask import Blueprint
from unique_number.database.db import get_db

rounds = Blueprint('rounds', __name__)

@rounds.route('/', methods=['GET'])
def get_rounds():
    db = get_db()
    result = db.query('SELECT * from person')
    print(list(result))

    return 'Hello World'
