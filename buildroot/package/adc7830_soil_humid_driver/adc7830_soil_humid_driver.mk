################################################################################
#
# adc7830_soil_humid_driver - out-of-tree Linux kernel module
#
################################################################################

ADC7830_SOIL_HUMID_DRIVER_VERSION = 1.0
ADC7830_SOIL_HUMID_DRIVER_SITE = https://github.com/KubaTaba1uga/kernel_ads7830_soil_humid_driver

# If you are developing locally, you can override the source:
ADC7830_SOIL_HUMID_DRIVER_OVERRIDE_SRCDIR = ../adc7830_soil_humid_driver

# Use the kernel module package infrastructure.
$(eval $(kernel-module))
$(eval $(generic-package))
