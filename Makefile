COMPOSE := docker compose
DAG ?= monthly_summary_etl

.PHONY: help
help:
	@echo "Доступные команды"
	@echo " make build - Билд docker образов"
	@echo " make up - Старт сервисов"
	@echo " make down - Остановка сервисов"
	@echo " make reset - Остановка сервисов и удаление всех volumes"
	@echo " make logs - смотреть логи"
	@echo " make run-dag - запустить DAG в Airflow (DAG=<dag_id>)"
	@echo " make lint - линтер кода"
	@echo " make format - отформатировать код"
	@echo " make test - запустить тесты"

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
	$(COMPOSE) logs -f --tail=200

.PHONY: run-dag
run-dag:
	$(COMPOSE) exec -T airflow-api-server airflow dags unpause $(DAG) || true
	$(COMPOSE) exec -T airflow-api-server airflow dags trigger $(DAG)

.PHONY: lint
lint:
	ruff check .
	ruff format . --check
	mypy

.PHONY: format
format:
	ruff check . --fix
	ruff format .

.PHONY: test
test:
	pytest
