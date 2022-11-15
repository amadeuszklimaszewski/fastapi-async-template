# fastapi-async-template
FastAPI template to speed up the development process. Uses library `asyncpg` and SQLAlchemy async engine. Docker creates a second database for testing purposes. Tests include `conftest.py` file with needed setup to run tests in an asynchronous manner.

## Tech stack
* FastAPI `0.87.0`
* SQLAlchemy `1.4.44`
* Alembic `1.8.1`
* PostgreSQL `14.2`
* Docker

## Setup
1. Clone repository:
`$ git clone https://github.com/amadeuszklimaszewski/fastapi-async-template`
2. Run in root directory:
`$ make build-dev`
3. Provide `AUTHJWT_SECRET_KEY` in .env file
4. Run template: `$ make up-dev`

## Migrations
Run `$ make migrations` to migrate.

## Tests
`$ make test`

## Makefile
`Makefile` contains useful command aliases

## Docs
SwaggerUI docs available at `localhost:8000/docs`
