#!/bin/bash
#
set -euo pipefail  # Exit on error

aarch64-linux-gnu-gcc src/main.c -o ads7830_soil_humid_sensor_driver
# gcc src/main.c -o ads7830_soil_humid_sensor_driver -l:libi2c.a
