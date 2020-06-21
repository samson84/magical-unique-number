# unique-number

A simple guess the least unique positive integer number implementation.

## Usage

### Prerequisites

The following components are needed for the fluent working environment.

- install docker: https://docs.docker.com/get-docker/
- install docker-compose: https://docs.docker.com/compose/install/
- install poetry (for development): https://python-poetry.org/docs/

Tested with the following versions:

- Python: 3.8.3
- Pip: 19.2.3
- Docker: 19.03.11 build 42e35e61f3
- Docker Compose: 1.26.0, build d4451659
- Linux/Mint/Ubuntu(18.04)
- Chrome: 83, Firefox: 77

### Start the application

The full environment is managed by docker compose it will spin up a database and the service too.

1. Check the `example.env` file, create an `.env` file based on that. (The database will be created with those values.)
2. Install the needed components in the prerequisites section.
3. `make start-production` to start the application.
4. Reach the api on `localhost:APP_EXTERNAL_PORT` (APP_EXTERNAL_PORT is set up in the `.env` file.) 
5. Open `localhost:APP_EXTERNAL_PORT/game` in your borwser for the game. (Only latest Firefox and Chrome is supported.)
6. Test the proper setup: `curl localhost:APP_EXTERNAL_PORT/rounds`. `{payload: []}` should be received.

- Check the logs: `make production-logs`
- Stop the application: `make stop-production`

### Manage the project

Check the Makefile for available commands. Even if no Makefile is used, the general usage of the repo is documented there.

### Configuration and package management

`.env` file is used by the application "inside" and by the docker outside.

The package management is poetry, so the `requirements.txt` is git ignored.
The dependencies are listed in the `pyproject.toml`, the deep dependency tree is freezed in `poetry.lock`. If a new dependency is added to the project, a lockfile should be updated with `make update-dependencies`.

Hovewer when the app's container is built by docker, it uses the `requriements.txt`, it is generated from the `poetry.lock` with the `make create-requirements-txt`. This makefile target is called automatically when
start-production targer is invoked.

### Database initalization

The DB init sql is located in `./sql/init`. When first time the docker spin up the environment, all the sql scripts are executed from this location to the DB.

The data is persistent in a docker volume between the container restarts, however if the related docker volume is deleted, the data will be lost.

## Development

### Set up a development environment

1. `make install-dev`
2. `make run-dev-server`

### Running integration tests

Currently only integration tests are available. The integration tests uses a
real postgre db. They fill it with test data defined in the scripts, and
remove the data after the test case is executed.

Test's environment variables are defined in the `test.env`.

A running postgre instance is needed for the tests, and its settings 
must match with the `test.env`.

Two make targets optionally create the test server based on the `test.env` file.

`make start-dev-db`

`make stop-dev-db`

To run the test

`make run-tests`

### Using test data for development

Some random test data found in `./sql/test_data.sql`. The `init.sql` must be executed first.

### Planning and design

The design decisions and a short REST API design document is 
in the [design.md](design.md).

## PM

### Requirements

- [x] Single Global Playground
- [x] Trusted players (no registration)
- [x] Explicit start of a round
- [x] Within an active round:
  - [x] A user can add their number with a name as part of the game. The name is unique and cannot be reused in the round.
  - [x] All users vote is collected.
- [x] Compete the Round, return roundID
- [x] Round Results: winner, and the number
- [x] Listing all rounds with IDs and start date, end date, number of participants
- [x] Querying the results of any rounds including the most recent one: Winner and winning number
- [x] Querying the statistics of any round: distribution of votes from 1 to the max number voted for in that round.

### Tasks

- [x] create project skeleton
- [x] create Flask skeleton
  - [x] basic development runtime env
  - [x] routes and blueprints
  - [x] config
  - [x] error handling
  - [x] input validation
  - [x] add integration tests
- [x] database: postgresql
  - [x] create a running database
  - [x] integrate the db access to Flask
  - [x] create a data access layer
  - [x] develop a scheme
  - [x] create scheme sql
  - [x] create test data
- [x] REST API 
  - [x] design
  - [x] `HTTP GET /rounds`: list rounds
  - [x] `HTTP POST /rounds`: create a new round
  - [x] `HTTP POST or PUT /rounds/<id>/finish`: finish a given round
  - [x] `HTTP POST /rounds/<id>/vote`: add a new vote to an active round
  - [x] `HTTP GET /rounds/<id>`: get the one round document
  - [x] `HTTP GET /rounds/<id>/stat`: get a stat document
- [x] static file serving
- [x] frontend
- [x] deployment to production

## Purpose

The project was made for an exercise for a job interview. On the other hand, I wanted to make a Flask boilerplate for future use and also wanted to practice the SQL queries and REST API design.

