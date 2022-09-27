RUN=poetry run

all:
	docker-compose build

run:
	docker-compose up

shell:
	docker-compose run --rm ml-assistant /bin/bash

fmt:
	black .
	isort . --profile black

lint:
	black . --check
	isort . -c --profile black

test:
	$(RUN) pytest -x -vvv --pdb

report:
	$(RUN) pytest -x --pdb

report-fail:
	$(RUN) pytest --cov-report term --cov-fail-under=90
