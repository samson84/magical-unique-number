import pytest

from utils import (
    create_vote_queries,
    create_round_queries,
    app_test_context,
    MatchString
)

def test_it_should_start_a_new_round():        
    input_rounds = create_round_queries([
        (None, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00'),
    ])
    input_votes = create_vote_queries([
        (1, 1, 5, 'daniel'),
        (2, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    expected = {
        'payload': {
            'id': 2,
            'started_at': MatchString(),
            'finished_at': None,
            'participants': 0,
            'winner_username': None,
            'winner_vote': None,
            '_links': {
                'self': {'href': '/rounds/2'}, 
                'stat': {'href': '/rounds/2/stat'}
            }
        }
    }

    with app_test_context(input_data) as client:
        client.post('/rounds', json={})
        current = client.get('/rounds/2').get_json()
    assert current == expected
