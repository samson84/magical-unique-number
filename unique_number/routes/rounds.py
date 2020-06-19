from flask import Blueprint, request
from datetime import datetime

from unique_number.models import rounds, votes
from unique_number.utils.responses import create_success
from unique_number.utils import errors, validator

rounds_blueprint = Blueprint('rounds', __name__)

VOTE_MIN_VALUE = 1
VOTE_MAX_VALUE = 2147483646 # max int in postgre sql

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

@rounds_blueprint.route('/<int:round_id>/vote', methods=['POST'])
@validator.validate_json({
    'type': 'object', 
    'properties': {
        'username': {'type': 'string'},
        'vote': {'type': 'number'}
    },
    'required': ['username', 'vote']
})
def handle_vote(round_id):
    data = request.json
    vote = data.get('vote')
    username = data.get('username')

    if vote < VOTE_MIN_VALUE:
        raise errors.InvalidVote(f'Your vote should be at least {VOTE_MIN_VALUE}.')
    if vote > VOTE_MAX_VALUE:
        raise errors.InvalidVote(f'Your vote should be at most {VOTE_MAX_VALUE}.')
    if votes.is_voted(round_id, username):
        raise errors.InvalidVote(f'You have already voted.')
    
    current_round = rounds.get_one_round(round_id)
    if current_round is None:
        raise errors.NotFound('Round for vote')
    if current_round['finished_at'] is not None:
        raise errors.InvalidVote(f'The round is already finished.')

    votes.add_vote(round_id, username, vote)

    return create_success({})

@rounds_blueprint.route('/<int:round_id>/stat', methods=['GET'])
def handle_stats(round_id: int):
    current_round = rounds.get_one_round(round_id)
    if current_round is None:
        raise errors.NotFound('Round for stats')
    if current_round['finished_at'] is None:
        raise errors.RoundStillActive()
    stats = votes.get_stats(round_id)
    return create_success(stats)



