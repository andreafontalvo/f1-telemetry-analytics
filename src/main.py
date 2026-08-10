# from src.ingestion.openf1_client import OpenF1Client


# def main():
#     client = OpenF1Client()

#     meeting = client.get_meeting(year=2025,country_name="Belgium")

#     print("Meeting:")
#     print(meeting)

#     session = client.get_race_session(meeting_key=meeting["meeting_key"])

#     print("\nRace session:")
#     print(session)

#     car_data_driver = client.get_car_data(session_key=session["session_key"],driver_number=44)

#     print("\nCar data:")
#     print(f"Retrieved {len(car_data_driver)} telemetry records")


# if __name__ == "__main__":
#     main()

from src.ingestion.telemetry_ingestion import TelemetryIngestion


def main():
    ingestion = TelemetryIngestion()

    ingestion.ingest_race(
        year=2025,
        country_name="Netherlands",
    )


if __name__ == "__main__":
    main()