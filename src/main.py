from src.ingestion.telemetry_ingestion import TelemetryIngestion
from src.analytics.telemetry_analysis import TelemetryAnalysis


def main():

    year = 2025
    country_name = "Spain"
    driver = "VER"

    # -------------------------
    # Data ingestion
    # -------------------------

    ingestion = TelemetryIngestion()
    race_dir = ingestion.ingest_race(year=year,country_name=country_name)

    # -------------------------
    # Spark analytics
    # -------------------------

    analysis = TelemetryAnalysis()

    # race_name = f"{country_name.lower()}_grand_prix"
    # telemetry_path = (
    #     f"/app/data/raw/{year}/"
    #     f"{race_name}/race/"
    #     f"telemetry/{driver}")
    telemetry_path = race_dir / "telemetry" / driver
    race_name = race_dir.parent.name

    df = analysis.load_driver_telemetry(telemetry_path)

    clean_df = analysis.clean_telemetry(df)

    analysis.inspect(clean_df)
    analysis.quality_check(clean_df)
    analysis.basic_metrics(clean_df)

    metrics_by_gear = analysis.metrics_by_gear(clean_df)

    analysis.plot_speed_by_gear(metrics_by_gear,year=year,race=race_name,driver=driver)

    analysis.stop()


if __name__ == "__main__":
    main()