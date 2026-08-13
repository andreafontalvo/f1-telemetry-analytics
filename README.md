# F1 Telemetry Analytics

A data engineering project focused on analyzing Formula 1 car telemetry data using Python, Apache Spark, Docker, and OpenF1 API.

The project is designed to strengthen distributed data processing skills and explore an IoT Data Engineering use case based on high-frequency sensor data.

## Project Goals

* Acquire Formula 1 telemetry data from the OpenF1 API.
* Build a reproducible data ingestion pipeline.
* Store and reuse downloaded telemetry data through a local cache.
* Process and analyze telemetry data using Apache Spark.
* Explore transformations and aggregations over high-volume sensor data.

## Data Source

Telemetry data is provided by [OpenF1](https://openf1.org/).

The project currently focuses on **Race** sessions and uses the `car_data` endpoint, which provides measurements such as:

* Speed
* RPM
* Throttle
* Brake
* Gear
* DRS
* Timestamp
* Driver number

## Architecture

Downloaded telemetry is stored locally and reused on subsequent executions. Before requesting a chunk from the API, the ingestion pipeline checks whether the corresponding JSON file already exists. This makes the ingestion process restartable. If a run is interrupted, the pipeline does not need to download already completed chunks again.

```text
                         OpenF1 API
                              │
                              ▼
                    Python Ingestion Layer
                              │
                    ┌─────────┴─────────┐
                    │                   │
              Race metadata       Driver telemetry
                    │                   │
                    │          Time-based chunks
                    │             (10 min)
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       Local JSON Cache
                              │
                              ▼
                       Apache Spark
                              │
                              ▼
                    Telemetry Analytics
```

## Project Structure

```text
f1-telemetry-analytics/
│
├── data/
│   └── raw/
│       └── <year>/
│           └── <grand_prix>/
│               └── race/
│                   ├── meeting.json
│                   ├── session.json
│                   ├── drivers.json
│                   │
│                   └── telemetry/
│                       ├── VER/
│                       │   ├── chunk_000.json
│                       │   ├── chunk_001.json
│                       │   ├── chunk_002.json
│                       │   └── ...
│                       │
│                       ├── NOR/
│                       │   ├── chunk_000.json
│                       │   ├── chunk_001.json
│                       │   └── ...
│                       │
│                       └── ...
│
├── src/
│   ├── ingestion/
│   │   ├── openf1_client.py
│   │   └── telemetry_ingestion.py
│   │
│   └── main.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```


## Running the Project

Build the Docker image:

```bash
docker compose build
```

Run the ingestion pipeline:

```bash
docker compose run --rm f1-telemetry
```

Downloaded telemetry is stored locally and reused on executions through the cache.

## Updates
### August 2026
* Added OpenF1 API client.
* Added automatic selection of meetings by year + country.
* Added automatic selection of the Race session.
* Added automatic discovery of all drivers participating in the race.
* Added car_data telemetry ingestion.
* Changed telemetry ingestion from full-session requests to 10-minute time-based chunks.
* Added per-driver telemetry storage.
* Added per-chunk local caching.
* Added retry logic with exponential backoff for OpenF1 API rate limits.
* Added Docker-based development environment.

## Current Status

### Phase 1 — Data Ingestion

* [x] Project structure
* [x] Docker environment
* [x] OpenF1 API client
* [x] Meeting and race session selection
* [x] Driver discovery
* [x] Car telemetry ingestion
* [x] Local telemetry cache

### Phase 2 — Spark Analytics

* [x] Read telemetry with Spark
* [x] Explore Spark DataFrames
* [ ] Clean and transform telemetry
* [ ] Driver-level aggregations
* [ ] Telemetry analytics
* [ ] Spark SQL / window functions
