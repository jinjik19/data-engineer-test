# Тестовое задание DE

Решение тестового задания на позицию Data Engineer

В задании реализован локальный ETL-пайплайн для загрузки CSV-данных в ClickHouse, подготовки данных в staging-слое и построение аналитической витрины.

Витрина используется для визуализации в Metabase:

- помесячной динамики депозитов, выводов и ставок;
- распределение метрик по странам;
- табличное представление итоговой витрины.

Более подробно про тестовое можно почитать в файле: [docs/Описание ДЗ Data Engineer.pdf](docs/Описание%20ДЗ%20Data%20Engineer.pdf)

## Стек

- Clickhouse
- Airflow
- Python3.13
- Metabase
- Docker Compose
- Pandas/Jupyter

## Архитектура

CSV Files -> Airflow ETL -> raw слой -> staging слой -> monthly_summary витрина -> Metabase dashboard

## Слои данных

### Raw слой

Слой загрузки исходных данных из CSV файлов.

Данные из CSV загружаются в `raw.*` с техническими полями:

- `source_file` - имя исходного файла
- `load_id` - id запуска DAG
- `loaded_at` - время загрузки строки

Также создана таблица `load_batches`, в которой хранится информация об успешных загрузках.
Повторный запуск DAG добавляет новые строки в `raw` с новым `load_id`.
Это ожидаемое поведение, так как, raw слой хранит историю загрузок и позволяет отследить какие данные были загружены в каждом запуске. Плюс так как в `raw` используется движок `ReplacingMergeTree`, то данные этих таблиц тоже рано или поздно в фоне будут дедуплицированны.

### Staging cлой

staging - это слой для дедуплицированных данных из `raw` Строится из последних успешных загрузок в `raw`.

### Mart слой

mart - это слой для построения витрин данных. Все витрины будут строится из данных полученных из `staging` слоя.

## Структура проекта

- config/ - настройки Airflow
- dags/ — DAG файлы Airflow
- data/ - исходные CSV файлы
- docker/ - докерфайлы
  - docker/airflow - докерфайл airflow
- docs/ - различные документация по проекту
- notebooks/ - исследование данных
- plugins/ -
- sql/ - sql скрипты
  - sql/init/ — инициализация бд и raw таблиц в clickhouse
  - sql/staging/ - sql скрипты для создания таблиц в staging слое
  - sql/mart/ - sql скрипты для построения витрин данных
  - sql/checks - sql скрипты для проверки данных в хранилище

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
```

2. Запустить сервисы:

```bash
make up
```

После запуска будут доступны:

Airflow: [http://localhost:8080](http://localhost:8080)
логин и пароль из .env файла. По умолчанию для локальных запусков - airflow/airflow

Metabase: [http://localhost:3000](http://localhost:3000)
логин и пароль по умолчанию для локальных запусков: admin@example.com/admin12345

3. Посмотреть логи

```bash
make logs
```

4. Запуск DAG

DAG называется `monthly_summary_etl`

```bash
make run-dag
```

5. Остановить сервисы

```bash
make down
```

6. Остановить сервисы и удалить volumes

```bash
make reset
```

## Metabase

Metabase использует H2 БД, сохранённую в репозитории в `metabase/data`.
Я это сделал для тестового проекта, чтобы после `docker compose up` сразу было готовое подключение к ClickHouse и дашборд без ручной настройки Metabase.
В production я бы так не делал, но для локального тестового проекта выбрал простой и воспроизводимый вариант.

Также мои сохраненые графики можно посмотреть тут - [docs/Metabase - витрина monthly summary.pdf](./docs/Metabase%20-%20витрина%20monthly%20summary.pdf)

## Локальная разработка

Версия Python зафиксирована в `.python-version`. Используется версия 3.13

### Linux

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

### Windows

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

### Make команды для разработки

Проверить код линтером и форматтером:

```bash
make lint
```

Отформатировать код:

```bash
make format
```

Запустить тесты:

```bash
make test
```
