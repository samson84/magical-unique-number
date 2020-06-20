default: install-dev run-dev-server

install-dev:
	poetry install

update-dependencies:
	poetry update

create-requirements-txt:
	poetry export --format requirements.txt --output requirements.txt

run-dev-server:
	poetry run python main.py

run-tests:
	poetry run pytest -vv tests/

start-test-db:
	docker-compose --file docker-compose.test.yml --env-file test.env up --detach

stop-test-db:
	docker-compose --file docker-compose.test.yml --env-file test.env down

start-production: create-requirements-txt
	docker-compose --env-file .env up --detach

stop-production:
	docker-compose down

production-logs:
	docker-compose logs -f