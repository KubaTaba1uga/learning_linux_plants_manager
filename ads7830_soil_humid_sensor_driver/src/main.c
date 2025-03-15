/*
 #################################
 #          Imports              #
 #################################
*/
#include <fcntl.h>
#include <i2c/smbus.h>
#include <linux/i2c-dev.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <unistd.h>

/*
 #################################
 #          Macros               #
 #################################
*/
#define BUS_NUMBER "1"
#define ADS_ADDR 0x48
#define CONVERSION_REG 0b00000000
#define CONFIG_REG 0b00000001
#define LOW_REG 0b00000010
#define HIGH_REG 0b00000011
#define VOLTAGE_REF 3.3
#define MAX_VALUE 26250

/*
 #################################
 #      Static declarations      #
 #################################
*/
static int configure_continuous_conversion(int bus);
static float val_to_voltage(u_int16_t value);

/*
 #################################
 #         Public API            #
 #################################
 */
int main(void) {
  const char *filename = "/dev/i2c-" BUS_NUMBER;
  u_int8_t buffer[2];
  u_int16_t result;
  int bus;

  if ((bus = open(filename, O_RDWR)) < 0) {
    perror("Failed to open the i2c bus");
    exit(1);
  }

  if (ioctl(bus, I2C_SLAVE, ADS_ADDR) < 0) {
    perror("Failed to specify ADS1115 as device to communicate to");
    exit(2);
  }

  if (configure_continuous_conversion(bus) != 0) {
    perror("Failed to configure continuos converion mode on ADS1115");
    exit(3);
  };

  /* memset(buffer, 0, 2); */

  /* while (true) { */
  /*   if (read(bus, buffer, 2) != 2) { */
  /*     perror("Failed to read data from ADS1115"); */
  /*     exit(3); */
  /*   } */

  /*   result = (buffer[0] << 8) | buffer[1]; */

  /*   printf("ADC Value: %i Voltage: %.2f V\n", result,
   * val_to_voltage(result)); */

  /*   usleep(500000); // half a second */
  /* } */

  return 0;
}

/*
 #################################
 #         Private API           #
 #################################
*/
int configure_continuous_conversion(int bus) {
  u_int8_t buffer[3];

  // Set Low Threshold register as active
  buffer[0] = LOW_REG;
  if (write(bus, buffer, 1) != 1) {
    perror("Failed to activate low threshold register");
    return 1;
  };

  // Write to Low Threshold register
  buffer[0] = LOW_REG;
  buffer[1] = 0b01000000;
  buffer[2] = 0b00000000;
  if (write(bus, buffer, 3) != 3) {
    perror("Failed to write data to low threshold register");
    return 2;
  };

  // Set High Threshold register as active
  buffer[0] = HIGH_REG;
  if (write(bus, buffer, 1) != 1) {
    perror("Failed to activate high threshold register");
    return 3;
  };
  // Write to High Threshold register
  buffer[0] = HIGH_REG;
  buffer[1] = 0b01111111;
  buffer[2] = 0b11111111;
  if (write(bus, buffer, 3) != 3) {
    perror("Failed to write data to high threshold register");
    return 4;
  };

  // Set Config register as active
  buffer[0] = CONFIG_REG;
  if (write(bus, buffer, 1) != 1) {
    perror("Failed to activate Config register");
    return 5;
  };
  buffer[0] = CONFIG_REG;
  // MUX sets schannel from which values will be read.
  //            x100xxxx - sets channel 0 as active and GND as reference point
  //            xxxx001x - sets gain apmlifier equal +/- 4.096V
  buffer[1] = 0b01000010;
  //            011xxxxx - sets data rate 64SPS
  //            xxxxxx11 - disables comparator
  buffer[2] = 0b01100011;
  if (write(bus, buffer, 3) != 3) {
    perror("Failed to write data to Config register");
    return 6;
  };

  // Set Conversion register as active
  buffer[0] = CONVERSION_REG;
  if (write(bus, buffer, 1) != 1) {
    perror("Failed to activate Conversion register");
    return 7;
  };

  return 0;
}

float val_to_voltage(__u16 value) {
  return (float)value / MAX_VALUE * VOLTAGE_REF;
}
