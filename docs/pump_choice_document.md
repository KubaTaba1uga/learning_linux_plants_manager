## Small plants

For small plants we use:
- https://www.amazon.com/Kamoer-Peristaltic-Hydroponics-Nutrient-Analytical/dp/B07GWJ78FN

## Big plants

If we want to use 5l canister as irrigation src, we may need to lift liquid few meters we may need better pump like:
- https://www.amazon.com/peristaltic-KPHM200-Laboratory-High-Precision-OD%EF%BC%8C200ml/dp/B09HGVLHFV?ref_=ast_sto_dp&th=1

## How to control the pumps 
The Raspberry Pi GPIO only outputs 3.3V at max ~16mA, not enough to power or switch devices like a 12V 1A pump (12W). So you need external powert source for the pump and the driver. A driver circuit acts as an electronic switch controlled by the Pi to turn the high-power load on/off using an external 12V power source.

Driver:
- https://botland.com.pl/sterowniki-silnikow-dc/7043-drv8871-jednokanalowy-sterownik-silnikow-45v36a-adafruit-3190-5904422335373.html

Power source:
- https://botland.com.pl/zasilacze-dogniazdkowe/7155-zasilacz-impulsowy-12v25a-100v-240v-wtyk-dc-5525mm-5904422375409.html

For more info look here on photo:
![photo](https://cdn3.botland.com.pl/26468-pdt_540/drv8871-jednokanalowy-sterownik-silnikow-45v36a-adafruit-3190.jpg)
