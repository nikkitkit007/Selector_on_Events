include .env

CODE = $(APPLICATION_NAME) server

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif


APPLICATION_NAME = ITMO_events

run:
	docker-compose -f docker-compose.yml up

migrate:  ##@Database Do all migrations in database
	cd data_base && alembic upgrade $(args)

clear_db:  ##@Database Do all migrations in database
	cd data_base && alembic downgrade -1 &&  alembic upgrade +1

db:
	psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} ${POSTGRES_DB}

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

help:
	@echo "relax!!!"