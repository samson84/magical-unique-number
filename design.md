# Design of the application

## Technologies

- Python / Flask
- Package management: Poetry
- Database: Postgre
- Deployment: Docker ?

## REST API design

Based on: https://restfulapi.net/rest-api-design-tutorial-with-example/

### Object Model

- Rounds
- Stats of a round

### Model URIs

- `/rounds`: collection
- `/rounds/<id>`: document, metadata + results
- `/rounds/<id>/finish`: controller, finish the round
- `/rounds/<id>/vote`: controller, vote to an active round
- `/roduns/<id>/stat`: (sub)document

### Representations

#### Rounds collection

```json
[
    // finished
    {
        "id": 1234,
        "started_at": "2020-06-18T15:22:02Z", // ISO8601 UTC
        "finished_at": "2020-06-18T15:22:02Z", //ISO8601 UTC
        "participants": 136,
        "_links": {
            "self": {"href": "/rounds/1234"}
        },
    },
    // ongoing
    {
        "id": 1235,
        "started_at": "2020-06-18T15:22:02Z", // ISO8601 UTC
        "finished_at": null, //ISO8601 UTC
        "participants": null,
        "_links": {
            "self": {"href": "/rounds/1235"}
        },
    }
]
```

#### Single Round resource

```json
// finished
{
    "id": 1234,
    "started_at": "2020-06-18T15:22:02Z", // ISO8601 UTC
    "finished_at": "2020-06-18T15:22:02Z", //ISO8601 UTC
    "participants": 42,
    "winner_name": "Ford",
    "winner_vote": 5,
    "_links": {
        "self": {"href": "/rounds/1234"},
        "stat": {"href": "/rounds/1234/stat"},
    },
}
```

```json
// ongoing
{
    "id": 1235,
    "started_at": "2020-06-18T15:22:02Z", // ISO8601 UTC
    "finished_at": null,
    "participants": null,
    "winner_name": null,
    "winner_vote": null,
    "_links": {
        "self": {"href": "/rounds/1235"}
    }

}
```

#### Single Stat document

```json
// finished 
{
    "round_id": 1234,
    "votes": [
        [1, 15], // [vote, number of items]
        [2, 30],
        [5, 43],
        [7, 1]
    ],
    "_links": {
        "self": {"href": "/rounds/1234/stat"},
        "round": {"href": "/rounds/1234"}
    }
}
```

### HTTP Methods

- `HTTP GET /rounds`: list rounds
  - [x] returns: round collection or empty list
  - [x] 200: OK
- `HTTP POST /rounds`: create a new round
  - [x] returns: round document
  - [x] 200: OK
- `HTTP POST or PUT /rounds/<id>/finish`: finish a given round
  - [x] returns: round document
  - [x] 200: OK
  - [x] 404: if the <id> does not exists
  - [x] 409: Conflict, if the round has already finished
- `HTTP POST /rounds/<id>/vote`: add a new vote to an active round
  - returns: empty
  - 200: OK
  - 409: if the round has already finished
  - 409: if the user already voted
  - 404: if the round does not exists
- `HTTP GET /rounds/<id>`: get the one round document
  - [x] returns: a round document
  - [x] 200: OK
  - [x] 404: If the round does not exists
- `HTTP GET /rounds/recent`: get the recent one
  - [x] returns: a round document
  - [x] 200: OK
  - [x] 404: If the round does not exists
- `HTTP GET /rounds/<id>/stat`: get a stat document
  - returns: a stat document
  - 200: OK
  - 409: Conflict, If the round is ongoing.
  - 404: If the round does not exists

## DB Scheme

- ROUND table
  - id: int, primary key, auto increment
  - started_at: datetime in UTC
  - finished_at: datetime in UTC
  - winner_vote_id: int, foreign key -> ROUND
- VOTE table
  - id: int, primary key, auto increment
  - round_id: int, foreign key -> ROUND
  - vote: int
  - user: string (max 100)
  - 
