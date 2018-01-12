#!/usr/bin/env bash
''''export PYTHONPATH=/Library/Python/2.7/site-packages # '''
# find the latest python interpreter available
''''which python3 >/dev/null 2>&1 && exec python2 "$0" "$@" # '''
''''which python2 >/dev/null 2>&1 && exec python2 "$0" "$@" # '''
''''which python  >/dev/null 2>&1 && exec python  "$0" "$@" # '''
''''exec echo "Error: Unable to find python interpreter"    # '''

import httplib2
import os
import re
import sys
from datetime import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES             = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIAL_FILE    = 'gmail-usps-uniquify.json'
APPLICATION_NAME   = 'Gmail USPS Uniquify'


rest = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)
    client_secret_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
    if os.path.exists(CLIENT_SECRET_FILE):
        os.rename(CLIENT_SECRET_FILE, client_secret_path)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def messages():
    global rest
    if not rest:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        rest = service.users().messages()
    return rest

def get_message_info(message):
    id   = message['id']
    info = messages().get(userId='me',id=id,format='full').execute()

    subject = ''
    date    = ''
    for header in info['payload']['headers']:
        if header['name'] == 'Subject':
            subject = header['value']
        if header['name'] == 'Date':
            date = header['value']
        if subject and date:
            break

    return type('',(object,),{
        'id': message['id'],
        'internalDate': info['internalDate'],
        'date': date,
        'subject': subject
    })() # return an anonymous object

def send_to_trash(message):
    result = messages().trash(userId='me',id=message.id).execute()

def ts():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def write_log(message):
    print(ts() + ' ' + message)
    sys.stdout.flush()


def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """

    write_log('Started.')
    results = messages().list(
        userId='me',
        q='from:auto-reply@usps.com Shipment',
        includeSpamTrash=False
    ).execute()

    seen = {}
    shipment_number = re.compile(r"Shipment\s+((?:[0-9]+|[0-9]+[a-zA-Z]+|[a-zA-Z]+[0-9]+)[0-9a-zA-Z]*)")
    if not results:
        write_log('No USPS messages found.')
    else:
        count = results['resultSizeEstimate']
        write_log(str(count) + ' messages found; filtering')
        for msg in results['messages']:
            info = get_message_info(msg)
            shipment = shipment_number.search(info.subject).group(1)
            if shipment not in seen:
                seen[shipment] = info
            else:
                if seen[shipment].internalDate <= info.internalDate:
                    write_log("'"+seen[shipment].subject+"' superceded by")
                    write_log("    '"+info.subject+"'")
                    send_to_trash(seen[shipment])
                    seen[shipment] = info
                else:
                    write_log("'"+info.subject+"' superceded by")
                    write_log("    '"+seen[shipment].subject+"'")
                    send_to_trash(info)
        # for
    # if not results
    write_log('Done.')

if __name__ == '__main__':
    main()
