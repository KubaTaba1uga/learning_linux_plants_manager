import os
import sqlite3
import time
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

this_script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.environ.get("SENSORS_DB_PATH") or "/opt/sensors.db"
app = FastAPI()

app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(this_script_dir, "frontend"), html=True),
    name="frontend",
)


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like row access
    return conn


@app.get("/sensors")
def read_sensors(max_time_range: int = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM sensor_data"
    params = []
    if max_time_range is not None:
        # Calculate the cutoff timestamp (assuming max_time_range is in hours)
        cutoff_unix = int(time.time()) - max_time_range * 60 * 60
        cutoff_iso = datetime.fromtimestamp(cutoff_unix).strftime("%Y-%m-%dT%H:%M:%S")

        query += " WHERE timestamp >= ?"
        params.append(cutoff_iso)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    data = [dict(row) for row in rows]
    return {"data": data}


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open(os.path.join(this_script_dir, "frontend", "index.html"), "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
