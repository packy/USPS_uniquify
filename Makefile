PROJECT=gmail-usps-uniquify

all:
	cp $(PROJECT).py $(PROJECT)-cron.sh $(HOME)/bin/
	chmod +x $(HOME)/bin/$(PROJECT).py
	chmod +x $(HOME)/bin/$(PROJECT)-cron.sh
	sudo cp com.packay.$(PROJECT).plist /Library/LaunchDaemons
	launchctl start /Library/LaunchDaemons/com.packay.$(PROJECT).plist
