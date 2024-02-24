install:
	pip install poetry && \
	poetry install

run:
	docker-compose build && \
	docker-compose up

build:
	docker-compose build

up:
	docker-compose up

test:
	pytest -vx --cov=app --cov-report term-missing --cov-fail-under=95

data_test:
	echo wip

alembic_reset:
	docker-compose run app alembic downgrade base

migrate_down:
	docker-compose run app alembic downgrade -1

migrate_up:
	docker-compose run app alembic upgrade +1

migration:
	docker compose run app alembic revision --autogenerate -m "$(msg)"

migrate_head:
	docker compose run app alembic upgrade head

format:
	black .

generate_sdk:
	npm install
	python sdk_client_script.py
	npm run generate-client
