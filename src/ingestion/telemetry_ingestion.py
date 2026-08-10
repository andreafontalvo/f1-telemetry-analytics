import json
from pathlib import Path

from src.ingestion.openf1_client import OpenF1Client


class TelemetryIngestion:
    def __init__(self, data_dir="data/raw"):

        self.client = OpenF1Client()
        self.data_dir = Path(data_dir)


    def ingest_race(self, year, country_name):

        meeting = self.client.get_meeting(year=year,country_name=country_name)
        session = self.client.get_race_session(meeting_key=meeting["meeting_key"])
        drivers = self.client.get_drivers(session_key=session["session_key"])

        # print("MEETING:")
        # print (meeting)

        # print("SESSION:")
        # print(session)

        # print("DRIVERS:")
        # print(drivers)


        race_dir = (
            self.data_dir
            / str(year)
            / meeting["meeting_name"].lower().replace(" ", "_")
            / "race"
        )

        race_dir.mkdir(parents=True, exist_ok=True)

        self._save_json(
            meeting,
            race_dir / "meeting.json"
        )

        self._save_json(
            session,
            race_dir / "session.json"
        )

        self._save_json(
            drivers,
            race_dir / "drivers.json"
        )

        for driver in drivers:
            driver_number = driver["driver_number"]
            acronym = driver["name_acronym"]

            output_file = race_dir / f"car_data_{acronym}.json"

            if output_file.exists():
                print(f"[CACHE] {acronym}: already downloaded")
                continue

            print(
                f"[DOWNLOAD] {acronym} "
                f"(car #{driver_number})"
            )

            car_data = self.client.get_car_data(session_key=session["session_key"],driver_number=driver_number)

            self._save_json(car_data,output_file)

            print(f"{len(car_data)} telemetry records")

    def _save_json(self, data, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )