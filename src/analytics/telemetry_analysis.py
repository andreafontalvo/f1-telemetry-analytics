from pathlib import Path
from pyspark.sql import SparkSession


class TelemetryAnalysis:

    def __init__(self):

        self.spark = (SparkSession.builder.appName("F1 Telemetry Analytics").getOrCreate())


    def load_driver_telemetry(self, path):

        telemetry_dir = Path(path)
        files = [str(file) for file in telemetry_dir.glob("*.json")]
        if not files:
            raise FileNotFoundError(f"No telemetry files found in {telemetry_dir}")

        print("\n=== Telemetry files ===")
        for file in files:
            print(file)

        df = self.spark.read.json(files)
        return df


    def inspect(self, df):  

        print("\n=== Schema ===")
        df.printSchema()

        print("\n=== Record count ===")
        print(df.count())

        print("\n=== Sample ===")
        df.show(10, truncate=False)

        print("\n=== Statistics ===")
        df.describe().show()

    def stop(self):
        self.spark.stop()