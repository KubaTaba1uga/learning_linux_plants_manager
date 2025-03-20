################################################################################
#
# adc7830_soil_humid_driver - out-of-tree Linux kernel module
#
################################################################################

ADC7830_SOIL_HUMID_DRIVER_VERSION = 1.0
ADC7830_SOIL_HUMID_DRIVER_SITE = http://www.foosoftware.org/download

# If you are developing locally, you can override the source:
ADC7830_SOIL_HUMID_DRIVER_OVERRIDE_SRCDIR = ../adc7830_soil_humid_driver

# If additional options are needed for building, for example:
ADC7830_SOIL_HUMID_DRIVER_MAKE_OPTS = -j$(nproc)   # any additional options

# Declare dependency on the Linux kernel package so that the module is rebuilt if the kernel is changed.
ADC7830_SOIL_HUMID_DRIVER_DEPENDENCIES = linux

# Use the kernel module package infrastructure.
$(eval $(kernel-module))
$(eval $(generic-package))
