# linux_plants_manager

The project creates simple plants managment application on raspberry pi 5. Currently available features:
- None
<!-- - Monitor air temprature -->
<!-- - Monitor air humidity -->
<!-- - Monitor soil humidity -->

Hardware required to build the app:
- https://botland.store/multifunctional-sensors/2637-temperature-and-humidity-sensor-dht22-am2302-module-cables-5904422372712.html
- https://learn.adafruit.com/adafruit-ads7830-8-channel-8-bit-adc
- https://botland.store/raspberry-pi-5-modules-and-kits/25346-raspberry-pi-5-2gb-5056561803302.html
- https://mikrobot.pl/czujnik-wilgotnosci-gleby-v1-2-pojemnosciowy

## Install perequesites

To manage a project you need invoke python package. It can be installed on debian via
```
sudo apt install python3-invoke
```

## Build app

<TO-DO>

## Connect hardware

Connect ADS7830 to RPI 5:
- VIN pin to 5v power
- GND pin to GND
- SDA pin to GPIO 2
- SCL pin to GPIO 3

Image showing rpi pinnout can be found [here](https://pinout-ai.s3.eu-west-2.amazonaws.com/raspberry-pi-5-gpio-pinout-diagram.webp).

Image showing connecting rpi to ADS7830 can be found [here](https://cdn-learn.adafruit.com/assets/assets/000/125/868/original/adafruit_products_piBB_bb.jpg?1699283305).
