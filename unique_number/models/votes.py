from typing import Dict, Union
from unique_number.database.db import get_db

TABLE_NAME = 'votes'

Vote = Dict[str, Union[str, int]]
def create_vote(id: int, round_id: int, vote: int, username: str) -> Vote:
    return {
        'id': id,
        'round_id': round_id,
        'vote': vote,
        'username': username
    }

def get_winner(round_id):
    QUERY = f'''
        SELECT
            v.id,
            v.round_id,
            v.vote,
            v.username
        FROM {TABLE_NAME} v
        WHERE 
                v.round_id = %s
            AND
                v.vote = (
                    -- select the minimum unique vote
                    SELECT 
                        min(vote_counts.vote) min_vote
                    FROM (
                        -- count each vote
                        SELECT
                            vote,
                            count(vote) vote_count
                        FROM votes
                        WHERE
                                round_id = %s
                        GROUP BY
                            vote
                    ) vote_counts
                    WHERE vote_counts.vote_count = 1
                )
    '''
    results = get_db().query(QUERY, [round_id, round_id])
    result_list = list(results)
    if len(result_list) == 1:
        return create_vote(*result_list[0])
    else:
        return None

