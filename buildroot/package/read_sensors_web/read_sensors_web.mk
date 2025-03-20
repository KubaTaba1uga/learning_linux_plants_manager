READ_SENSORS_WEB_VERSION = 1.0
READ_SENSORS_WEB_SOURCE = read_sensors_web.py
READ_SENSORS_WEB_SITE_METHOD = local
READ_SENSORS_WEB_SITE = ../read_sensors_web
READ_SENSORS_WEB_DEPENDENCIES = python3
READ_SENSORS_WEB_DEPENDENCIES += python-fastapi
READ_SENSORS_WEB_DEPENDENCIES += python-uvicorn

define READ_SENSORS_WEB_INSTALL_TARGET_CMDS
	chmod 0755 $(@D)/read_sensors_web.py
	cp $(@D)/read_sensors_web.py $(TARGET_DIR)/usr/bin
endef

$(eval $(generic-package))
