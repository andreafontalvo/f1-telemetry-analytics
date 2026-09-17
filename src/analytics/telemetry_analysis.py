from pathlib import Path
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    when,
    to_timestamp,
    avg,
    max
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

    # def clean_telemetry(self, df):
    #     clean_df = (df.withColumn("date", to_timestamp("date")))
    #     return clean_df

    def clean_telemetry(self, df):
        clean_df = (
            df
            .withColumn("date", to_timestamp("date"))
            .withColumn(
                "throttle",
                when(col("throttle") <= 100, col("throttle"))
            )
            .withColumn(
                "brake",
                when(col("brake") <= 100, col("brake"))
            )
        )

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

        print("\n=== Throttle values above 100 ===")

        df.filter(col("throttle") > 100).select(
            "date",
            "throttle",
            "speed",
            "rpm",
            "brake"
        ).show(20, truncate=False)


        print("\n=== Brake values above 100 ===")

        df.filter(col("brake") > 100).select(
            "date",
            "brake",
            "speed",
            "rpm",
            "throttle"
        ).show(20, truncate=False)


    def inspect(self, df):  
        print("\n=== Schema ===")
        df.printSchema()
        print("\n=== Record count ===")
        print(df.count())
        print("\n=== Sample ===")
        df.show(10, truncate=False)
        print("\n=== Statistics ===")
        df.describe().show()


    def basic_metrics(self, df):
        print("\n=== Basic Metrics ===")
        metrics = df.agg(
            max("speed").alias("max_speed"),
            avg("speed").alias("avg_speed"),
            max("rpm").alias("max_rpm"),
            avg("rpm").alias("avg_rpm"),
            avg("throttle").alias("avg_throttle"),
            avg("brake").alias("avg_brake")
        )
        metrics.show()


    def metrics_by_gear(self, df):
        print("\n=== Metrics by Gear ===")

        metrics = (
            df.groupBy("n_gear").agg(
                avg("speed").alias("avg_speed"),
                max("speed").alias("max_speed")
            ) .orderBy("n_gear"))

        metrics.show()
        return metrics


    def plot_speed_by_gear(self, metrics, year, race, driver):
        rows = metrics.collect()

        gears = [row["n_gear"] for row in rows]
        avg_speed = [row["avg_speed"] for row in rows]
        max_speed = [row["max_speed"] for row in rows]

        plt.figure(figsize=(10, 6))

        plt.plot(gears,avg_speed,marker="o",label="Average speed")
        plt.plot(gears,max_speed,marker="o",label="Maximum speed")

        plt.xlabel("Gear")
        plt.ylabel("Speed (km/h)")
        plt.title(f"{driver}: speed by gear ({year} {race})")

        plt.xticks(gears)
        plt.legend()
        plt.grid(True)

        plt.tight_layout()

        plt.savefig(f"/app/data/processed/speed_by_gear_{year}_{race}_{driver}.png")
        print(f"\n=== Speed by Gear plot saved at /app/data/processed/speed_by_gear_{year}_{race}_{driver}.png ===")

        plt.close()
    
    
    def stop(self):
        self.spark.stop()
