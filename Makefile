COMPOSE := docker compose

.PHONY: help
help:
	@echo "Доступные команды"
	@echo " make build - Билд docker образов"
	@echo " make up - Старт сервисов"
	@echo " make down - Остановка сервисов"
	@echo " make reset - Остановка сервисов и удаление всех volumes"
	@echo " make logs - смотреть логи"

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