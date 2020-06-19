from flask import Blueprint

from unique_number.models import rounds
from unique_number.utils.responses import create_success
from unique_number.utils import errors

rounds_blueprint = Blueprint('rounds', __name__)

@rounds_blueprint.route('/', methods=['GET'])
def get_rounds():
    results = rounds.get_all_rounds()
    return create_success(list(results))

@rounds_blueprint.route('/<int:round_id>', methods=['GET'])
def get_one_round(round_id: int):
    result = rounds.get_one_round(round_id)
    
    if result is None:
        raise errors.NotFound(what = 'Round')
    
    return create_success(result)