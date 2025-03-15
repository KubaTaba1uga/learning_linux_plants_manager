#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <unistd.h>

#define I2C_BUS "/dev/i2c-1"
#define ADS7830_ADDR 0x48

int main(void) {
  int bus_fd = open(I2C_BUS, O_RDWR);
  if (bus_fd < 0) {
    perror("Failed to open the i2c bus");
    return 1;
  }

  if (ioctl(bus_fd, I2C_SLAVE, ADS7830_ADDR) < 0) {
    perror("Failed to set slave address");
    close(bus_fd);
    return 1;
  }

  // Send the control byte for single-ended, channel 0, power-down mode
  uint8_t config = 0x80; // (1000 0000)
  if (write(bus_fd, &config, 1) != 1) {
    perror("Failed to configure ADS7830");
    close(bus_fd);
    return 1;
  }

  // Read back the ADC value (8 bits)
  uint8_t adc_val;
  if (read(bus_fd, &adc_val, 1) != 1) {
    perror("Failed to read from ADS7830");
    close(bus_fd);
    return 1;
  }

  printf("ADC reading = %d\n", adc_val);

  close(bus_fd);
  return 0;
}
