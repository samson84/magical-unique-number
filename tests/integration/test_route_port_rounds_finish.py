import pytest

from utils import (
    create_vote_queries,
    create_round_queries,
    app_test_context,
    MatchString
)

def test_it_should_finish_a_new_round():        
    input_rounds = create_round_queries([
        (None, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00'),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    expected = {
        'payload': {
            'id': 2,
            'started_at': MatchString(),
            'finished_at': MatchString(),
            'participants': 1,
            'winner_username': 'john',
            'winner_vote': 1,
            '_links': {
                'self': {'href': '/rounds/2'}, 
                'stat': {'href': '/rounds/2/stat'}
            }
        }
    }

    with app_test_context(input_data) as client:
        client.post('/rounds', json={})
        client.post('/rounds/2/vote', json={'username': 'john', 'vote': 1})
        client.post('/rounds/2/finish', json={})
        current = client.get('/rounds/2').get_json()
    assert current == expected

def test_it_should_get_error_if_the_round_id_not_exists():
    input_rounds = create_round_queries([
        (None, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00'),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    expected = {'error': {'code': 'not_found', 'message': MatchString()}}

    with app_test_context(input_data) as client:
        current = client.post('/rounds/6/finish', json={}).get_json()
    assert current == expected

def test_it_should_get_error_if_the_round_already_finished():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00'),
    ])
    input_votes = create_vote_queries([
        (1, 1, 5, 'daniel'),
        (2, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    expected = {'error': {'code': 'already_finished', 'message': MatchString()}}

    with app_test_context(input_data) as client:
        current = client.post('/rounds/1/finish', json={}).get_json()
    assert current == expected
