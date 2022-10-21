include .env

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

db:
	psql -h 127.0.0.1 -p 5435 -U postgres ITMO_Event

help:
	@echo "relax!!!"