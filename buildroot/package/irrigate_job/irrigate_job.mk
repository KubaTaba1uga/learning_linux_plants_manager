IRRIGATE_JOB_VERSION = 1.0
IRRIGATE_JOB_SOURCE = irrigate_job.py
IRRIGATE_JOB_SITE_METHOD = local
IRRIGATE_JOB_SITE = ../irrigate_job
IRRIGATE_JOB_DEPENDENCIES = python3

CRON_DIR = $(TARGET_DIR)/etc/cron/crontabs
CRON_FILE = $(CRON_DIR)/root
CRON_LINE = 0 */12 * * * python3 /opt/irrigate_job.py

define IRRIGATE_JOB_INSTALL_TARGET_CMDS
	chmod 0755 $(@D)/irrigate_job.py
	cp $(@D)/irrigate_job.py $(TARGET_DIR)/opt

	# Ensure the cron directory exists
	if [ ! -d "$(CRON_DIR)" ]; then \
	  mkdir -p "$(CRON_DIR)"; \
	fi

	# Ensure the cron file exists
	if [ ! -f "$(CRON_FILE)" ]; then \
	  touch "$(CRON_FILE)"; \
	fi

	# Append the job line if missing
	grep -qxF "$(CRON_LINE)" "$(CRON_FILE)" || echo "$(CRON_LINE)" >> "$(CRON_FILE)"
endef

$(eval $(generic-package))
