from src.ingestion.telemetry_ingestion import TelemetryIngestion
from src.analytics.telemetry_analysis import TelemetryAnalysis


def main():

    year = 2025
    country_name = "Spain"

    # -------------------------
    # Data ingestion
    # -------------------------

    ingestion = TelemetryIngestion()

    ingestion.ingest_race(
        year=year,
        country_name=country_name)

    # -------------------------
    # Spark analytics
    # -------------------------

    analysis = TelemetryAnalysis()

    telemetry_path = (
        f"/app/data/raw/{year}/"
        f"spanish_grand_prix/race/"
        f"telemetry/VER"
    )

    df = analysis.load_driver_telemetry(telemetry_path) 
    clean_df = analysis.clean_telemetry(df)

    analysis.inspect(clean_df)
    analysis.quality_check(clean_df)
    analysis.basic_metrics(clean_df)
    analysis.metrics_by_gear(clean_df)

    analysis.stop()


if __name__ == "__main__":
    main()