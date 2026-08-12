import json
from pathlib import Path
from src.ingestion.openf1_client import OpenF1Client
from datetime import datetime, timedelta

CHUNK_MINUTES = 10

class TelemetryIngestion:


    def __init__(self, data_dir="data/raw"):

        self.client = OpenF1Client()
        self.data_dir = Path(data_dir)


    def ingest_race(self, year, country_name):

        meeting = self.client.get_meeting(year=year,country_name=country_name)
        session = self.client.get_race_session(meeting_key=meeting["meeting_key"])
        drivers = self.client.get_drivers(session_key=session["session_key"])

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

            driver_dir = race_dir / "telemetry" / acronym

            driver_dir.mkdir(parents=True,exist_ok=True)

            print(
                f"[DRIVER] {acronym} "
                f"(car #{driver_number})"
            )

            self.download_driver_telemetry(session=session,driver=driver,driver_dir=driver_dir)


    def _save_json(self, data, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data,file,indent=2,ensure_ascii=False)


    def download_driver_telemetry(self, session, driver, driver_dir):
        session_key = session["session_key"]
        driver_number = driver["driver_number"]
        acronym = driver["name_acronym"]

        start = datetime.fromisoformat(session["date_start"])
        end = datetime.fromisoformat(session["date_end"])

        current = start
        chunk_number = 0

        while current < end:

            chunk_end = min(current + timedelta(minutes=CHUNK_MINUTES),end)

            output_file = driver_dir / f"chunk_{chunk_number:03d}.json"

            # Cache
            if output_file.exists():
                print(
                    f"[CACHE] {acronym} "
                    f"chunk {chunk_number:03d}"
                )

                current = chunk_end
                chunk_number += 1
                continue

            print(
                f"[DOWNLOAD] {acronym} "
                f"{current.isoformat()} → {chunk_end.isoformat()}"
            )

            chunk = self.client.get_car_data_chunk(
                session_key=session_key,
                driver_number=driver_number,
                start_time=current.isoformat(),
                end_time=chunk_end.isoformat(),
            )

            print(f"    {len(chunk)} records")

            # save CHUNK
            self._save_json(chunk,output_file)

            current = chunk_end
            chunk_number += 1