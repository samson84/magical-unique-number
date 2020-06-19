from typing import Dict, Union, List, Tuple
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

Stat = Dict[str, Union[List, int, str]]
def create_stat(round_id: int, votes: List[Tuple[int, int]]) -> Stat:
    return {
        "round_id": round_id,
        "votes": votes,
        "_links": {
            "self": {"href": f"/rounds/{round_id}/stat"},
            "round": {"href": f"/rounds/{round_id}"}
        }
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

def is_voted(round_id: int, username: str) -> bool:
    QUERY = f'''
        SELECT
            COUNT({TABLE_NAME})
        FROM {TABLE_NAME}
        WHERE round_id=%s AND username=%s
    '''
    results = get_db().query(QUERY, [round_id, username])
    result_list = list(results)
    if len(result_list) == 1:
        return result_list[0][0] != 0
    else:
        return False

def add_vote(round_id: int, username: str, vote: int) -> int:
    QUERY = f'''
        INSERT INTO {TABLE_NAME} (round_id, username, vote) 
        VALUES (%s, %s, %s) 
        RETURNING id'''
    result = get_db().query(QUERY, [round_id, username, vote])
    return list(result)[0][0]

def get_stats(round_id: int) -> Stat:
    QUERY = f'''
        SELECT 
            vote,
            COUNT(vote) count
        FROM {TABLE_NAME}
        WHERE round_id=%s
        GROUP BY vote
    '''
    result = get_db().query(QUERY, [round_id])
    vote_stats = list(result)
    return create_stat(round_id, vote_stats)
