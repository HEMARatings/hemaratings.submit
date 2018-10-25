COMPOSE_DEV=docker-compose -f docker-compose.yml

lint:
	flake8 backend
	pydocstyle backend

build:
	$(COMPOSE_DEV) up -d --build backend


run-dev:
	$(COMPOSE_DEV) up
