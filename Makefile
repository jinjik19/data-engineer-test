COMPOSE := docker compose

.PHONY: help
help:
	@echo "Доступные команды"
	@echo " make build - Билд docker образов"
	@echo " make up - Старт сервисов"
	@echo " make down - Остановка сервисов"
	@echo " make reset - Остановка сервисов и удаление всех volumes"
	@echo " make logs - смотреть логи"
	@echo " make lint - линтер кода"
	@echo " make format - отформатировать код"

.PHONY: build
build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

.PHONY: down
down:
	$(COMPOSE) down

.PHONY: reset
reset:
	$(COMPOSE) down -v

.PHONY: logs
logs:
	$(COMPOSE) logs -f

.PHONY: lint
lint:
	ruff check .
	ruff format . --check
	mypy

.PHONY: format
format:
	ruff check . --fix
	ruff format .
