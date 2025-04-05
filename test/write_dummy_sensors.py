import sqlite3
from datetime import datetime

DB_PATH = "/opt/sensors.db"
PLANTS = 4  # Adjust this to simulate more/less plants

# Moisture values: plants 0–3 = 40%, others = 80%
sensor_values = [40 if i < 4 else 80 for i in range(PLANTS)]

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    columns = ",\n".join([f"sensor{i} INTEGER" for i in range(1, PLANTS + 1)])
    create_stmt = f"""
        CREATE TABLE IF NOT EXISTS sensor_data (
            timestamp TEXT,
            {columns}
        );
    """
    cursor.execute(create_stmt)

    # Insert dummy row
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now] + sensor_values
    placeholders = ", ".join(["?"] * len(row))
    cursor.execute(f"INSERT INTO sensor_data VALUES ({placeholders})", row)

    conn.commit()
    conn.close()

    print(f"Inserted dummy data for {PLANTS} plants: {row}")

except Exception as e:
    print(f"Error writing dummy sensor data: {e}")
