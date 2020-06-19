from typing import NamedTuple, Iterable, Union, Dict, Optional
from datetime import datetime

from unique_number.database.db import get_db
from unique_number.models import votes

TABLE_NAME = 'rounds'

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
            "self": {"href": "/rounds/1234"},
            "stat": {"href": "/rounds/1234/stat"},
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
        ;
    """
    results = get_db().query(QUERY)
    for row in results:
        yield create_round_list_item(*row)

def get_one_round(_id: int) -> Union[RoundItem, None]:
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
        ;
    """
    results = get_db().query(QUERY, [_id])
    results_list = list(results)
    if len(results_list) == 1:
        round_item = create_round_item(*results_list[0])
        if round_item['finished_at'] is not None:
            winner = votes.get_winner(round_item['id'])
            return create_round_item(*results_list[0], winner=winner)
        return round_item
    else:
        return None



