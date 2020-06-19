import pytest

from utils import (
    create_vote_queries,
    create_round_queries,
    app_test_context
)

def test_it_should_get_recent_round():        
    input_rounds = create_round_queries([
        (1, '2020-08-11 13:30:39+00', '2020-08-12 13:30:39+00'),
        (2, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00')
    ])
    input_votes = create_vote_queries([
        (2, 2, 5, 'daniel')
    ])
    input_data = input_rounds + input_votes
    expected = {
        'payload': {
            'id': 2,
            'started_at': '2019-08-11T13:30:39+0000',
            'finished_at': '2019-08-12T13:30:39+0000',
            'participants': 1,
            'winner_username': 'daniel',
            'winner_vote': 5,
            '_links': {
                'self': {'href': '/rounds/2'}, 
                'stat': {'href': '/rounds/2/stat'}
            }
        }
    }

    with app_test_context(input_data) as client:
        current = client.get('/rounds/recent').get_json()
    assert current == expected

def test_it_should_get_recent_round_unfinished():
    input_rounds = create_round_queries([
        (1, '2020-08-11 13:30:39+00', '2020-08-12 13:30:39+00'),
        (2, '2019-08-11 13:30:39+00', None)
    ])
    input_votes = create_vote_queries([
        (2, 2, 5, 'daniel')
    ])
    input_data = input_rounds + input_votes
    expected = {
        'payload': {
            'id': 2,
            'started_at': '2019-08-11T13:30:39+0000',
            'finished_at': None,
            'participants': 1,
            'winner_username': None,
            'winner_vote': None,
            '_links': {
                'self': {'href': '/rounds/2'}, 
                'stat': {'href': '/rounds/2/stat'}
            }
        }
    }

    with app_test_context(input_data) as client:
        current = client.get('/rounds/recent').get_json()
    assert current == expected

