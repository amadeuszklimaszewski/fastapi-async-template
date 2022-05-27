postgres-user = postgres
postgres-database = postgres


build-dev:
	-cp -n ./config/.env.template ./.env
	docker-compose build

up-dev:
	docker-compose run --rm web bash -c "alembic upgrade head"
	docker-compose up

migrations:
	docker-compose run --rm web bash -c "alembic revision --autogenerate"
	docker-compose run --rm web bash -c "alembic upgrade head"
	
bash:
	docker-compose exec web bash

db-bash:
	docker-compose exec db bash

db-shell:
	docker-compose exec db psql -U $(postgres-user)

test:
	docker-compose exec web bash -c "pytest -s $(location)"
