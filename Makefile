default: install-dev run-dev-server

install-dev:
	poetry install

update-dependencies:
	poetry update

create-requirements-txt:
	poetry export -f requirements.txt

run-dev-server:
	poetry run python start-dev.py

run-tests:
	poetry run pytest -vv tests/

start-test-db:
	docker-compose --file docker-compose.test.yml --env-file test.env up --detach

stop-test-db:
	docker-compose --file docker-compose.test.yml --env-file test.env down