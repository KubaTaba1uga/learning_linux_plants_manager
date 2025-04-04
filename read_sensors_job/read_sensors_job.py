import datetime
import sqlite3
import logging

PLANTS = 4

# Configure logging to file
logging.basicConfig(
    filename="/var/log/read_sensors_job.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

db_path = "/opt/sensors.db"

# Define file paths for sensor data
soil_humid_path = (
    "/sys/devices/platform/axi/1000120000.pcie/1f00074000.i2c/i2c-1/1-0048/humidity"
)
air_humid_path = "/sys/devices/platform/am2303_device/humidity"
air_temp_path = "/sys/devices/platform/am2303_device/temperature"


def read_sensor_value(file_path):
    """Read and return the sensor value from a given file as an integer."""
    for _ in range(5):
        try:
            with open(file_path, "r") as f:
                value = int(f.read().strip())
                return value
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
    logging.error(f"Failed to read sensor value from {file_path} after multiple attempts.")
    return -1


# Read sensor values from the files
soil_humids = []
for i in range(PLANTS):
    sensor_file = f"{soil_humid_path}_{i}"
    soil_humids.append(read_sensor_value(sensor_file))

air_humid = read_sensor_value(air_humid_path)
air_temp = read_sensor_value(air_temp_path)

# Generate a timestamp for the record
timestamp = datetime.datetime.now().isoformat()

# Connect to SQLite database (creates it if it doesn't exist)
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
except Exception as e:
    logging.error(f"Database connection error: {e}")
    raise

# Create the table if it doesn't exist with integer columns for sensor readings
create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS sensor_data (
        timestamp TEXT,
        {'\n'.join(f'soil_humid_{i} INTEGER,' for i in range(PLANTS))}
        air_humid INTEGER,
        air_temp INTEGER
    )
"""
try:
    cursor.execute(create_table_sql)
    conn.commit()
except Exception as e:
    logging.error(f"Error creating table: {e}")
    raise

placeholders = ', '.join('?' for _ in range(1+PLANTS+1+1))
insert_sql = f"INSERT INTO sensor_data VALUES ({placeholders})"
try:
    cursor.execute(insert_sql, (timestamp, *soil_humids, air_humid, air_temp))
    conn.commit()
    logging.info("Sensor data inserted into database successfully.")
except Exception as e:
    logging.error(f"Error inserting sensor data: {e}")
    raise

conn.close()

