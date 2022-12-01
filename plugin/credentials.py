import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client, file, tools

SCOPES = ['https://www.googleapis.com/auth/calendar']

def credentials_exist():
    # home_dir = os.path.expanduser('~')
    # credential_dir = os.path.join(home_dir, '.credentials')
    # credential_path = os.path.join(credential_dir, 'calendar-plugin.json')
    # return os.path.exists(credential_path)
    return os.path.exists('credentials.json')

def get_credentials():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# def get_credentials():
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     credential_path = os.path.join(credential_dir, 'calendar-plugin.json')
    
#     store = file.Storage(credential_path)
#     credentials = store.get()

#     # if not credentials or credentials.invalid:
#     #     if not os.path.exists(CLIENT_SECRET_FILE):
#     #         # Create client secret file
#     #         client_secret_file = {
#     #             "installed": {
#     #                 "client_id": CLIENT_ID,
#     #                 "project_id": PROJECT_ID,
#     #                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     #                 "token_uri": "https://accounts.google.com/o/oauth2/token",
#     #                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     #                 "client_secret": CLIENT_SECRET,
#     #                 "redirect_uris": ["http://localhost"]
#     #             }
#     #         }
            
#     #         # Create JSON file from dictionary
#     #         with open(CLIENT_SECRET_FILE, 'w') as outfile:
#     #             json.dump(client_secret_file, outfile)

#     #     flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#     #     flow.user_agent = APPLICATION_NAME
#     #     credentials = tools.run_flow(flow, store)
#     #     # print('Storing credentials to ' + credential_path)

#     return credentials
