# USPS_uniquify
If you're signed up for USPS Tracking® by email, you know how, if you don't
delete them immediately, the messages can pile up and you can't immediately
tell which is the latest update.

This tool connects to your GMail account using the GMail REST API, searches
for messages from `auto-reply@usps.com` that contain the word 'Shipment' in
the subject.  It keeps track of which messages refer to which shipments,
and if it finds a message referring to a shipment that it has seen a newer
message for, it moves the older message to the Trash.

This was built starting from Google's [GMail API Python
Quickstart](https://developers.google.com/gmail/api/quickstart/python).

## Setup
After cloning this repository, follow the instructions for [turning on the GMail
API](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name).
The instructions tell you to download a JSON file, move it to your working directory and rename it `client_secret.json`. When the script is first run,
it will move this file to a `$HOME/.credentials` directory that it will create,
and then it will launch your default browser and prompt you to give the script
permission to access your GMail account.
