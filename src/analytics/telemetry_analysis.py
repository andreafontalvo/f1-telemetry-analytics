from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    when,
    to_timestamp
)

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

    def clean_telemetry(self, df):
        clean_df = (df.withColumn("date", to_timestamp("date")))
        return clean_df


    def quality_check(self, df):
        print("\n===== Quality Check =====")
        
        print("\n=== Null values ===")

        null_counts = df.select([
            count(
                when(col(column).isNull(), column)
            ).alias(column)
            for column in df.columns
        ])

        null_counts.show()

        print("\n=== Value ranges ===")

        df.select(
            "speed",
            "rpm",
            "throttle",
            "brake",
            "n_gear",
            "drs"
        ).describe().show()

        print("\n=== Potentially invalid values ===")

        df.select(
            count(when(col("speed") < 0, True)).alias("negative_speed"),
            count(when(col("rpm") < 0, True)).alias("negative_rpm"),
            count(when(col("throttle") > 100, True)).alias("throttle_over_100"),
            count(when(col("brake") > 100, True)).alias("brake_over_100"),
            count(when(col("n_gear") > 8, True)).alias("gear_over_8")
        ).show()
    

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