# fastapi-async-template
FastAPI template to speed up the development process. SQLModel is used for defining tables. Uses library `asyncpg` and async engine provided by SQLAlchemy. Docker creates a second database for testing purposes. Tests include `conftest.py` file with needed setup to run tests in an asynchronous manner.

## Tech stack
* FastAPI `0.78.0`
* SQLModel `0.0.6`
* Alembic `1.7.7`
* Docker
* PostgreSQL `14.2`

## Setup
1. Clone repository:
`$ git clone https://github.com/amadeuszklimaszewski/amigoapi/`
2. Run in root directory:
`$ make build-dev`
3. Provide `AUTHJWT_SECRET_KEY` in .env file
4. Run template: `make up-dev`

## Migrations
* Register your models in `./src/settings/alembic.py` by importing your `models.py` file.
* Run `$ make migrations` to migrate.

## Tests
`$ make test`

## Makefile
`Makefile` contains useful command aliases
