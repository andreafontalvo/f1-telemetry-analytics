import requests
import time


class OpenF1Client:

    BASE_URL = "https://api.openf1.org/v1"

    def get_meeting(self, year, country_name):
        params = {
            "year": year,
            "country_name": country_name,
        }

        response = requests.get(f"{self.BASE_URL}/meetings",params=params)
        response.raise_for_status()

        meetings = response.json()

        if not meetings:
            raise ValueError(f"No meeting found for {country_name} in {year}")

        if len(meetings) > 1:
            raise ValueError(f"Multiple meetings found for {country_name} in {year}")
        return meetings[0]


    def get_race_session(self, meeting_key):
        params = {
            "meeting_key": meeting_key,
            "session_name": "Race",
        }

        response = requests.get(f"{self.BASE_URL}/sessions",params=params)
        response.raise_for_status()

        sessions = response.json()

        if not sessions:
            raise ValueError(f"No Race session found for meeting {meeting_key}")
        return sessions[0]


    def get_drivers(self, session_key):
        params = {
            "session_key": session_key,
        }

        response = requests.get(f"{self.BASE_URL}/drivers",params=params)
        response.raise_for_status()

        return response.json()

    def get_car_data(self, session_key, driver_number):
        params = {
            "session_key": session_key,
            "driver_number": driver_number,
        }

        response = requests.get(f"{self.BASE_URL}/car_data",params=params)
        response.raise_for_status()

        return response.json()


    # def get_car_data_chunk(
    #     self,
    #     session_key,
    #     driver_number,
    #     start_time,
    #     end_time,
    # ):
    #     params = {
    #         "session_key": session_key,
    #         "driver_number": driver_number,
    #         "date>": start_time,
    #         "date<": end_time,
    #     }

    #     response = requests.get(f"{self.BASE_URL}/car_data",params=params)

    #     if response.status_code == 404:
    #         return []

    #     response.raise_for_status()

    #     return response.json()

    def get_car_data_chunk(
        self,
        session_key,
        driver_number,
        start_time,
        end_time,
    ):
        params = {
            "session_key": session_key,
            "driver_number": driver_number,
            "date>": start_time,
            "date<": end_time,
        }

        max_retries = 7

        for attempt in range(max_retries):
            response = requests.get(
                f"{self.BASE_URL}/car_data",
                params=params
            )

            # no hay datos en este intervalo
            if response.status_code == 404:
                return []

            # demasiadas peticiones
            if response.status_code == 429:
                wait_time = 2 ** attempt

                print(
                    f"[RATE LIMIT] Waiting {wait_time}s..."
                )

                time.sleep(wait_time)
                continue

            response.raise_for_status()
            time.sleep(1)
            return response.json()

        raise RuntimeError(
            "OpenF1 rate limit persisted after "
            f"{max_retries} retries."
        )