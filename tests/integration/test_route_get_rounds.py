import pytest

from utils import (
    create_vote_queries,
    create_round_queries,
    app_test_context
)

def test_it_should_get_all_rounds():        
    input_rounds = create_round_queries([
        (1, '2019-08-11 13:30:39+00', '2019-08-12 13:30:39+00'),
        (2, '2020-08-13 13:30:39+00', None)
    ])
    input_votes = create_vote_queries([
        (1, 1, 5, 'daniel'),
        (2, 1, 4, 'john'),
        (3, 1, 4, 'emily'),
        (4, 1, 6, 'arthur'),
        (5, 2, 6, 'arthur'),
        (6, 2, 5, 'daniel'),
        (7, 2, 5, 'zeno'),
    ])
    input_data = input_rounds + input_votes
    expected = {
        'payload': [
            {
                'id': 2,
                'started_at': '2020-08-13T13:30:39+0000',
                'finished_at': None,
                'participants': 3,
                '_links': {
                    'self': {'href': '/rounds/2'}, 
                }
            },
            {
                'id': 1,
                'started_at': '2019-08-11T13:30:39+0000',
                'finished_at': '2019-08-12T13:30:39+0000',
                'participants': 4,
                '_links': {
                    'self': {'href': '/rounds/1'}, 
                }
            }
        ]
    }

    with app_test_context(input_data) as client:
        current = client.get('/rounds').get_json()
    assert current == expected
