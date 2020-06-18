default: install-dev run-dev-server

install-dev:
	poetry install

update-dependencies:
	poetry update

create-requirements-txt:
	poetry export -f requirements.txt

run-dev-server:
	poetry run bash -c 'export FLASK flask '

run-tests:
	poetry run pytest -v tests/
