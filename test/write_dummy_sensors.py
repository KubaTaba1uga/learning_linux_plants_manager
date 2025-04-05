import sqlite3
from datetime import datetime

DB_PATH = "/opt/sensors.db"
PLANTS = 4  # Number of soil sensors (plants)

# Dummy sensor values
sensor_values = [40 if i < PLANTS else 80 for i in range(PLANTS)]  # soil_humid_X
air_humid = 55
air_temp = 23

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build column names dynamically
    soil_columns = [f"soil_humid_{i}" for i in range(PLANTS)]
    all_columns = ["timestamp"] + soil_columns + ["air_humid", "air_temp"]

    # Create table if it doesn't exist
    columns_def = ",\n".join(
        [
            f"{col} INTEGER" if col != "timestamp" else f"{col} TEXT"
            for col in all_columns
        ]
    )
    create_stmt = f"CREATE TABLE IF NOT EXISTS sensor_data (\n{columns_def}\n);"
    cursor.execute(create_stmt)

    # Prepare and insert row
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now] + sensor_values + [air_humid, air_temp]
    placeholders = ", ".join(["?"] * len(row))
    cursor.execute(f"INSERT INTO sensor_data VALUES ({placeholders})", row)

    conn.commit()
    conn.close()

    print(f"✅ Inserted dummy sensor data: {dict(zip(all_columns, row))}")

except Exception as e:
    print(f"❌ Error writing dummy sensor data: {e}")
