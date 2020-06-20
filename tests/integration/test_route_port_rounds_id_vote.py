import pytest

from utils import (
    create_vote_queries,
    create_round_queries,
    app_test_context,
    MatchString
)

def test_it_should_vote():        
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote = {'username': 'zeno', 'vote': 1}
    expected = {'payload': {}}

    with app_test_context(input_data) as client:
        current = client.post('/rounds/1/vote', json=input_vote).get_json()
    assert current == expected

def test_it_should_vote_multiple_times():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote_1 = {'username': 'zeno', 'vote': 1}
    input_vote_2 = {'username': 'arthur', 'vote': 2}
    expected = {'payload': {}}

    with app_test_context(input_data) as client:
        client.post('/rounds/1/vote', json=input_vote_1)
        current = client.post('/rounds/1/vote', json=input_vote_2).get_json()
    assert current == expected

def test_it_should_fail_if_the_vote_is_negative():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote = {'username': 'zeno', 'vote': -1}
    expected = {
        'error': {
            'code': 'invalid_vote', 
            'message': MatchString('at least')
        }
    }
    with app_test_context(input_data) as client:
        current = client.post('/rounds/1/vote', json=input_vote).get_json()
    assert current == expected

def test_it_should_fail_if_the_vote_is_large():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote = {'username': 'zeno', 'vote': 1000000000000}
    expected = {
        'error': {
            'code': 'invalid_vote', 
            'message': MatchString('at most')
        }
    }
    with app_test_context(input_data) as client:
        current = client.post('/rounds/1/vote', json=input_vote).get_json()
    assert current == expected

def test_it_should_fail_if_already_voted():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote = {'username': 'daniel', 'vote': 5}
    expected = {
        'error': {
            'code': 'invalid_vote', 
            'message': MatchString('already voted')
        }
    }
    with app_test_context(input_data) as client:
        current = client.post('/rounds/1/vote', json=input_vote).get_json()
    assert current == expected

def test_it_should_fail_if_the_round_not_exists():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', None),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote = {'username': 'daniel', 'vote': 5}
    expected = {
        'error': {
            'code': 'not_found', 
            'message': MatchString()
        }
    }
    with app_test_context(input_data) as client:
        current = client.post('/rounds/2/vote', json=input_vote).get_json()
    assert current == expected

def test_it_should_fail_if_the_round_is_finished():
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', '2019-09-11 13:30:39+00'),
    ])
    input_votes = create_vote_queries([
        (None, 1, 5, 'daniel'),
        (None, 1, 4, 'john')
    ])
    input_data = input_rounds + input_votes
    input_vote = {'username': 'zeno', 'vote': 5}
    expected = {
        'error': {
            'code': 'invalid_vote', 
            'message': MatchString('finished')
        }
    }
    with app_test_context(input_data) as client:
        current = client.post('/rounds/1/vote', json=input_vote).get_json()
    assert current == expected
