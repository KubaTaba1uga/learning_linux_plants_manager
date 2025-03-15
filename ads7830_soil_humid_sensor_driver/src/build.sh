#!/bin/bash
set -euo pipefail  # Exit on error

if ! command -v gcc &> /dev/null; then
    sudo apt-get update && sudo apt-get install -y gcc
fi

gcc -o ads_7830_soil_humid_sensor_driver main.c
