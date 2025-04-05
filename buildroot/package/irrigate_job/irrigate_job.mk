IRRIGATE_JOB_VERSION = 1.0
IRRIGATE_JOB_SOURCE = irrigate_job.py
IRRIGATE_JOB_SITE_METHOD = local
IRRIGATE_JOB_SITE = ../irrigate_job
IRRIGATE_JOB_DEPENDENCIES = python3

IRRIGATE_JOB_CRON_DIR = $(TARGET_DIR)/etc/cron/crontabs
IRRIGATE_JOB_CRON_FILE = $(IRRIGATE_JOB_CRON_DIR)/root
IRRIGATE_JOB_CRON_LINE = 0 8 * * * python3 /opt/irrigate_job.py

define IRRIGATE_JOB_INSTALL_TARGET_CMDS
	echo ">>> Installing irrigate_job <<<"
	chmod 0755 $(@D)/irrigate_job.py
	cp $(@D)/irrigate_job.py $(TARGET_DIR)/opt

	mkdir -p $(IRRIGATE_JOB_CRON_DIR)
	touch $(IRRIGATE_JOB_CRON_FILE)
	grep -qxF '$(IRRIGATE_JOB_CRON_LINE)' $(IRRIGATE_JOB_CRON_FILE) || echo '$(IRRIGATE_JOB_CRON_LINE)' >> $(IRRIGATE_JOB_CRON_FILE)
endef

$(eval $(generic-package))
