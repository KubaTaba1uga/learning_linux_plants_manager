import logging
import sqlite3
import time

PLANTS = 4

# Setup logging
logging.basicConfig(
    filename="/var/log/irrigate_dry_plants_job.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# Config
DB_PATH = "/opt/sensors.db"
VALVE_SYSFS_PATH = "/sys/devices/platform/irrigation_controller"
MOISTURE_THRESHOLD = 50
WATERING_DURATION = 10  # seconds per watering burst (N)
WATERING_REPEATS = 6  # times to repeat watering (X)
DELAY_BETWEEN_WATERINGS = 10  # optional delay between repeats


def get_latest_readings():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
            return cursor.fetchone()
    except Exception as e:
        logging.error(f"Error retrieving sensor data: {e}")
        return None


def log_watering(valve_index, duration):
    try:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO watering_log (valve_index, duration, timestamp) VALUES (?, ?, ?)",
                (valve_index, duration, timestamp),
            )
            conn.commit()
    except Exception as e:
        logging.error(f"Failed to log watering for valve {valve_index}: {e}")


def water_plant(valve_index, duration):
    try:
        logging.info(f"Irrigating valve {valve_index} for {duration}s")
        with open(f"{VALVE_SYSFS_PATH}/valve_index", "w") as f:
            f.write(str(valve_index))
        with open(f"{VALVE_SYSFS_PATH}/time", "w") as f:
            f.write(str(duration))
        with open(f"{VALVE_SYSFS_PATH}/trigger", "w") as f:
            f.write("1")
        log_watering(valve_index, duration)
    except Exception as e:
        logging.error(f"Failed to irrigate valve {valve_index}: {e}")
        try:
            with open(f"{VALVE_SYSFS_PATH}/trigger", "w") as f:
                f.write("0")
        except Exception as e2:
            logging.error(f"Failed to stop irrigation for valve {valve_index}: {e2}")


def main():
    row = get_latest_readings()
    if not row:
        return

    soil_values = row[1 : 1 + PLANTS]
    dry_plants = [
        idx for idx, value in enumerate(soil_values) if value < MOISTURE_THRESHOLD
    ]

    if not dry_plants:
        logging.info("All plants are sufficiently moist.")
        return

    logging.info(f"Plants to irrigate: {dry_plants}")

    for i in range(WATERING_REPEATS):
        logging.info(f"Watering round {i + 1}/{WATERING_REPEATS}")
        for valve_index in dry_plants:
            water_plant(valve_index, WATERING_DURATION)
        if i < WATERING_REPEATS - 1:
            time.sleep(DELAY_BETWEEN_WATERINGS)


if __name__ == "__main__":
    main()
