import pytest

from utils import (
    create_vote_queries,
    create_round_queries,
    app_test_context,
    MatchString
)

def test_it_should_get_stats():        
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00'),
        (2, '2020-08-11 13:30:39+00', '2020-08-12 13:30:39+00')
    ])
    input_votes = create_vote_queries([
        (1, 1, 5, 'daniel'),
        (2, 1, 4, 'john'),
        (3, 1, 4, 'emily'),
        (4, 1, 6, 'arthur'),
    ])
    input_data = input_rounds + input_votes
    expected = {
        'payload': {
            "round_id": 1,
            "votes": [
                [4, 2],
                [5, 1],
                [6, 1]
            ],
            "_links": {
                "self": {"href": "/rounds/1/stat"},
                "round": {"href": "/rounds/1"}
            }
        }
    }

    with app_test_context(input_data) as client:
        current = client.get('/rounds/1/stat').get_json()
    assert current == expected

def test_it_should_fail_if_the_round_unfinished():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
        (2, '2020-08-11 13:30:39+00', '2020-08-12 13:30:39+00')
    ])
    input_votes = create_vote_queries([
        (1, 1, 5, 'daniel'),
        (2, 1, 4, 'john'),
        (3, 1, 4, 'emily'),
        (4, 1, 6, 'arthur'),
    ])
    input_data = input_rounds + input_votes
    expected = {
        'error': {'code': 'not_finished', 'message': MatchString()}
    }

    with app_test_context(input_data) as client:
        current = client.get('/rounds/1/stat').get_json()
    assert current == expected

def test_it_should_fail_if_the_round_not_exists():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
        (2, '2020-08-11 13:30:39+00', '2020-08-12 13:30:39+00')
    ])
    input_votes = create_vote_queries([
        (1, 1, 5, 'daniel'),
        (2, 1, 4, 'john'),
        (3, 1, 4, 'emily'),
        (4, 1, 6, 'arthur'),
    ])
    input_data = input_rounds + input_votes
    expected = {
        'error': {'code': 'not_found', 'message': MatchString()}
    }

    with app_test_context(input_data) as client:
        current = client.get('/rounds/6/stat').get_json()
    assert current == expected

