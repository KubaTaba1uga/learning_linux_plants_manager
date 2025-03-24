import datetime
import math
import os
import sqlite3

db_path = os.environ.get("SENSORS_DB_PATH") or "/opt/sensors.db"


# Create the sensor_data table if it doesn't exist.
create_table_sql = """
    CREATE TABLE IF NOT EXISTS sensor_data (
        timestamp TEXT,
        soil_humid_0 INTEGER,
        soil_humid_1 INTEGER,
        soil_humid_2 INTEGER,
        soil_humid_3 INTEGER,
        soil_humid_4 INTEGER,
        soil_humid_5 INTEGER,
        soil_humid_6 INTEGER,
        soil_humid_7 INTEGER,
        air_humid INTEGER,
        air_temp INTEGER
    )
"""

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(create_table_sql)
conn.commit()

# Define simulation parameters.
# Start 3 days ago, ending now, with a reading every hour.
start_dt = datetime.datetime.now() - datetime.timedelta(days=3)
end_dt = datetime.datetime.now()
delta = datetime.timedelta(hours=1)

records = []

# Generate dummy records.
while start_dt <= end_dt:
    # Round the current time to the hour: set minutes, seconds, microseconds to zero.
    rounded_time = start_dt.replace(minute=0, second=0, microsecond=0)
    t = (rounded_time - datetime.datetime(1970, 1, 1)).total_seconds() / 3600.0

    # Simulate 8 soil humidity sensors with phase offsets.
    soil_humids = [
        int(50 + 10 * math.sin((t + i * 3) * (2 * math.pi / 24))) for i in range(8)
    ]
    # Simulate air humidity and temperature.
    air_humid = int(60 + 15 * math.sin((t + 1) * (2 * math.pi / 24)))
    air_temp = int(20 + 5 * math.sin((t - 3) * (2 * math.pi / 24)))

    timestamp_str = rounded_time.isoformat()
    records.append((timestamp_str, *soil_humids, air_humid, air_temp))
    start_dt += delta

# Prepare and execute insertion of dummy records.
placeholders = ", ".join("?" for _ in range(1 + 8 + 1 + 1))
insert_sql = f"INSERT INTO sensor_data VALUES ({placeholders})"
cursor.executemany(insert_sql, records)
conn.commit()
conn.close()
