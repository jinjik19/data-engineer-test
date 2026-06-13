# Тестовое задание DE

Решение тестового задания на позицию Data Engineer

Проект загружает исходные CSV-файлы в ClickHouse, выполняет проверки качества данных, строит ежемесячную аналитическую витрину и визуализирует результат

Более подробно про тестовое можно почитать в файле: ./docs/Описание ДЗ Data Engineer.pdf

## Задача

- спроектировать структуру хранения данных
- загрузить данные из CSV в Clickhouse
- пересчитать финансовые показатели в USD
- агрегировать данные по месяцам и странам
- обеспечить идемпотеность ETL процесса при повторных запусках на тех же данных
- визуализировать динамику депозитов, выводов и ставок помесячно и распределение по странам
- все решение должно запускаться через docker compose

## Стек

- Clickhouse
- Airflow
- Python3.13
- Metabase
- Docker Compose
- Pandas/Jupyter

## Архитектура

CSV Files -> Airflow ETL -> Clickhouse raw таблицы -> Data quality -> monthly_summary -> Metabase dashboard

## Структура проекта

- config/ - настройки Airflow
- dags/ — DAG файлы Airflow
- data/ - исходные CSV файлы
- docker/ - докерфайлы
  - docker/airflow - докерфайлы airflow
- docs/ - различные документация по проекту
- notebooks/ - исследование данных
- plugins/ -
- sql/ - sql скрипты
  - sql/init/ — инициализация бд и raw таблиц в clickhouse

## Аномалии

- Есть несовпадения провайдеров в games и games map, причем совпадений очень мало. По хорошему надо бы уточнить а что считать источником истины

## Запуск проекта

Для запуска нужны:

- Docker
- Docker Compose

### Переменные окружения

Создать локальный `.env`:

```bash
cp .env.example .env
```

### Команды запуска

1. Собрать Docker-образы:

```bash
make build
# или
docker compose build
```

2. Запустить сервисы:

```bash
make up
# или
docker compose up -d
```

3. Посмотреть логи

```bash
make logs
# или
docker compose logs -f
```

4. Остановить сервисы

```bash
make down
# или
docker compose down
```

5. Остановить сервисы и удалить volumes

```bash
make reset
# или
docker compose down -v
```

### Доступы

Airflow UI - http://localhost:8080
логин и пароль из .env файла
(AIRFLOW_ADMIN_USERNAME/AIRFLOW_ADMIN_PASSWORD)

Clickhouse HTTP - доступен на порту 8123
логин и пароль из .env файла
(CLICKHOUSE_USER/CLICKHOUSE_PASSWORD)

### Локальная разработка

Версия Python зафиксированна в `.python-version`. Используется версия 3.13

#### Linux

1. Создание виртуального окружения

```bash
python3 -m venv .venv
```

2. Запуск виртуального окружения

```bash
source .venv\bin\activate
```

3. Установка пакетов

```bash
pip install -r requirements-dev.txt
```

#### Windows

1. Создание виртуального окружения

```bash
python -m venv .venv
```

2. Запуск виртуального окружения
   CMD

```cmd
.venv\Scripts\activate.bat
```

or

POWERSHELL

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Установка пакетов

```bash
pip install -r requirements-dev.txt
```
