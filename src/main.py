from src.ingestion.telemetry_ingestion import TelemetryIngestion

def main():
    ingestion = TelemetryIngestion()

    ingestion.ingest_race(
        year=2025,
        country_name="Netherlands",
    )


if __name__ == "__main__":
    main()