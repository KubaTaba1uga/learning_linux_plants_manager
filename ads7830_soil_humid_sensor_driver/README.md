# ads7830_soil_humid_sensor_driver

## Prepare driver

Install dependencies
```
sudo apt-get install libi2c-dev
```




## Prepare board

### Prepare kernel

To show i2c devices in /dev/ directory we need to configure i2c as builtin module.

Add in config.txt:
```
dtparam=i2c_arm=on
dtoverlay=i2c1-pi5
```

### Prepare buildroot

To handle i2c devices you need BR2_PACKAGE_I2C_TOOLS setting enabled.

### Detect ads7830


Assuming you connected to GPIO 2 & GPIO 3
```
i2cdetect -y 1
```

Should show
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

