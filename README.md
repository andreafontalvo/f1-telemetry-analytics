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

```text
OpenF1 API
     │
     ▼
Python ingestion
     │
     ▼
Local JSON cache
     │
     ▼
Apache Spark
     │
     ▼
Telemetry analysis
```


## Project Structure

```text
f1-telemetry-analytics/
│
├── data/
│   └── raw/                 # Downloaded telemetry data (ignored by Git)
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

* [ ] Read telemetry with Spark
* [ ] Explore Spark DataFrames
* [ ] Clean and transform telemetry
* [ ] Driver-level aggregations
* [ ] Telemetry analytics
* [ ] Spark SQL / window functions
