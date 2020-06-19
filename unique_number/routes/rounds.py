from flask import Blueprint
from datetime import datetime

from unique_number.models import rounds
from unique_number.utils.responses import create_success
from unique_number.utils import errors

rounds_blueprint = Blueprint('rounds', __name__)

@rounds_blueprint.route('/', methods=['GET'])
def handle_get_rounds():
    results = rounds.get_all_rounds()
    return create_success(list(results))

@rounds_blueprint.route('/recent', methods=['GET'])
def handle_get_recent_round():
    result = rounds.get_recent_round()
    
    if len(result) is None:
        raise errors.NotFound(what = 'Round')
    
    return create_success(result)

@rounds_blueprint.route('/<int:round_id>', methods=['GET'])
def handle_get_one_round(round_id: int):
    result = rounds.get_one_round(round_id)
    
    if result is None:
        raise errors.NotFound(what = 'Round')
    
    return create_success(result)

@rounds_blueprint.route('/', methods=['POST'])
def handle_start_round():
    round_id = rounds.create_round(datetime.utcnow())
    result = rounds.get_one_round(round_id)
    if result is None:
        raise errors.NotFound(what = 'Round')
    return create_success(result)

@rounds_blueprint.route('/<int:round_id>/finish', methods=['POST'])
def handle_finish_round(round_id):
    current = rounds.get_one_round(round_id)
    if current is None:
        raise errors.NotFound(what = 'Round')
    if current['finished_at'] is not None:
        raise errors.RoundAlreadyFinished()
    rounds.finish_round(round_id, datetime.utcnow())
    result = rounds.get_one_round(round_id)
    if result is None:
        raise errors.NotFound(what = 'Round')
    return create_success(result)
