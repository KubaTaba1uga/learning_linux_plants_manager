################################################################################
#
# irrigation_controller_driver - out-of-tree Linux kernel module
#
################################################################################

IRRIGATION_CONTROLLER_DRIVER_VERSION = 1.0
IRRIGATION_CONTROLLER_DRIVER_SITE = https://github.com/KubaTaba1uga/kernel_8channel_relay_module_driver

IRRIGATION_CONTROLLER_DRIVER_OVERRIDE_SRCDIR = ../irrigation_controller_driver

# Use the kernel module package infrastructure.
$(eval $(kernel-module))
$(eval $(generic-package))
