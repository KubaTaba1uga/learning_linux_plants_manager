READ_SENSORS_WEB_VERSION = 1.0
READ_SENSORS_WEB_SOURCE = read_sensors_web.py
READ_SENSORS_WEB_SITE_METHOD = local
READ_SENSORS_WEB_SITE = ../read_sensors_web
READ_SENSORS_WEB_DEPENDENCIES = python3
READ_SENSORS_WEB_DEPENDENCIES += python-fastapi
READ_SENSORS_WEB_DEPENDENCIES += python-uvicorn

# Define separate variables for the cron directory and file.
INIT_DIR = $(TARGET_DIR)/etc/init.d/

define READ_SENSORS_WEB_INSTALL_TARGET_CMDS
	chmod 0755 $(@D)/read_sensors_web.py
	cp -r $(@D)/read_sensors_web.py $(@D)/frontend $(TARGET_DIR)/opt

	# Ensure the init directory exists
	@if [ ! -d "$(INIT_DIR)" ]; then \
	  mkdir -p "$(INIT_DIR)"; \
	fi

	cp $(@D)/S50read_sensors_web $(INIT_DIR)/
endef

$(eval $(generic-package))
