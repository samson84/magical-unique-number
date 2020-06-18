# magical-unique-number

A simple guess the least unique positive integer number implementation.

## Manage the project

Check the Makefile for available commands.

## Requirements

- [ ] Single Global Playground
- [ ] Trusted players (no registration)
- [ ] Explicit start of a round
- [ ] Within an active round:
  - [ ] A user can add their number with a name as part of the game. The name is unique and cannot be reused in the round.
  - [ ] All users vote is collected.
- [ ] Compete the Round, return roundID
- [ ] Round Results: winner, and the number
- [ ] Listing all rounds with IDs and start date, end date, number of participants
- [ ] Querying the results of any rounds including the most recent one: Winner and winning number
- [ ] Querying the statistics of any round: distribution of votes from 1 to the max number voted for in that round.

## Tasks

- [x] create project skeleton
- [ ] create Flask skeleton
  - [ ] basic development runtime env
  - [ ] routes and blueprints
  - [ ] config
  - [ ] logging
  - [ ] error handling
  - [ ] input validation
- [ ] database: postgresql
  - [ ] create a running database
  - [ ] integrate the db access to Flask
  - [ ] create a data access layer
  - [x] develop a scheme
- [ ] REST API 
  - [x] design
  - [ ] `HTTP GET /rounds`: list rounds
  - [ ] `HTTP POST /rounds`: create a new round
  - [ ] `HTTP POST or PUT /rounds/<id>/finish`: finish a given round
  - [ ] `HTTP POST /rounds/<id>/vote`: add a new vote to an active round
  - [ ] `HTTP GET /rounds/<id>`: get the one round document
  - [ ] `HTTP GET /rounds/<id>/stat`: get a stat document
- [ ] static file serving
- [ ] frontend
- [ ] deployment production

