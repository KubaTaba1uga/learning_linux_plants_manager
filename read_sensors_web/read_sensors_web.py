import sqlite3

from fastapi import FastAPI

db_path = "/opt/sensors.db"
app = FastAPI()


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like row access
    return conn


@app.get("/sensors")
def read_sensors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data")
    rows = cursor.fetchall()
    conn.close()
    # Convert rows to list of dictionaries
    data = [dict(row) for row in rows]
    return {"data": data}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
