from typing import NamedTuple, Iterable, Union, Dict, Optional, List, Tuple
from datetime import datetime

from unique_number.database.db import get_db
from unique_number.models import votes

TABLE_NAME = 'rounds'
LIMIT_OF_LISTING = 100000

RoundListItem = Dict[str, Union[int, datetime, dict]]
def create_round_list_item(id: int, started_at: datetime, finished_at: datetime, participants: int)->RoundListItem:
    return {
        'id': id,
        'started_at': started_at,
        'finished_at': finished_at, 
        'participants': participants,
        '_links': {
            'self': {'href': f'/rounds/{id}'}
        }
    }

RoundItem = Dict[str, Union[int, datetime, dict]]
def create_round_item(
    id: int, 
    started_at: datetime, 
    finished_at: datetime, 
    participants: int, 
    winner: Optional[votes.Vote] = None)->RoundItem:

    if winner is None:
        winner = {}

    return {
        "id": id,
        "started_at": started_at,
        "finished_at": finished_at,
        "participants": participants,
        "winner_username": winner.get('username'),
        "winner_vote": winner.get('vote'),
        "_links": {
            "self": {"href": f"/rounds/{id}"},
            "stat": {"href": f"/rounds/{id}/stat"},
        },
    }

def get_all_rounds() -> Iterable[RoundListItem]:

    QUERY = f"""
        SELECT 
            r.id round_id, 
            r.started_at started_at, 
            r.finished_at finished_at,
            COUNT(v.round_id) participants
        FROM {TABLE_NAME} r
        LEFT JOIN {votes.TABLE_NAME} v ON r.id = v.round_id
        GROUP BY v.round_id, r.id
        ORDER BY r.id DESC
        LIMIT %s;
    """
    results = get_db().query(QUERY, [LIMIT_OF_LISTING])
    for row in results:
        yield create_round_list_item(*row)

def fill_round_item(results: List[Tuple]) -> Union[RoundItem, None]:
    results_list = list(results)
    if len(results_list) == 1:
        round_item = create_round_item(*results_list[0])
        if round_item['finished_at'] is not None:
            winner = votes.get_winner(round_item['id'])
            return create_round_item(*results_list[0], winner=winner)
        return round_item
    else:
        return None

def get_one_round(id: int) -> Union[RoundItem, None]:
    QUERY = f"""
        SELECT 
            r.id round_id, 
            r.started_at started_at, 
            r.finished_at finished_at,
            COUNT(v.round_id) participants
        FROM {TABLE_NAME} r
        LEFT JOIN {votes.TABLE_NAME} v ON r.id = v.round_id
        WHERE r.id = %s
        GROUP BY v.round_id, r.id
        LIMIT 1
        ;
    """
    results = get_db().query(QUERY, [id])
    return fill_round_item(results)
    
def get_recent_round() -> Union[RoundItem, None]:
    QUERY = f"""
        SELECT 
            r.id round_id, 
            r.started_at started_at, 
            r.finished_at finished_at,
            COUNT(v.round_id) participants
        FROM {TABLE_NAME} r
        LEFT JOIN {votes.TABLE_NAME} v ON r.id = v.round_id
        GROUP BY v.round_id, r.id 
        ORDER BY r.id DESC
        LIMIT 1
        ;
    """
    results = get_db().query(QUERY)
    return fill_round_item(results)

def has_active_round() -> int:
    QUERY = f'''
        SELECT COUNT({TABLE_NAME}) 
        FROM {TABLE_NAME}
        WHERE finished_at is NULL
    '''
    result = get_db().query(QUERY)
    return list(result)[0][0] != 0

def create_round(started_at: datetime) -> int:
    QUERY = f'''
        INSERT INTO {TABLE_NAME} (started_at) 
        VALUES (%s) 
        RETURNING id'''
    result = get_db().query(QUERY, [started_at])
    return list(result)[0][0]

def finish_round(round_id: int, finished_at: datetime) -> int:
    QUERY = f"UPDATE {TABLE_NAME} SET finished_at=%s WHERE id=(%s) RETURNING id"
    result = get_db().query(QUERY, (finished_at, round_id))
    return list(result)


