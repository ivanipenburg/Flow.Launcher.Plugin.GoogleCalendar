import os
from oauth2client import client, file, tools


def credentials_exist():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'calendar-plugin.json')
    return os.path.exists(credential_path)

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'calendar-plugin.json')
    
    store = file.Storage(credential_path)
    credentials = store.get()

    # if not credentials or credentials.invalid:
    #     if not os.path.exists(CLIENT_SECRET_FILE):
    #         # Create client secret file
    #         client_secret_file = {
    #             "installed": {
    #                 "client_id": CLIENT_ID,
    #                 "project_id": PROJECT_ID,
    #                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #                 "token_uri": "https://accounts.google.com/o/oauth2/token",
    #                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #                 "client_secret": CLIENT_SECRET,
    #                 "redirect_uris": ["http://localhost"]
    #             }
    #         }
            
    #         # Create JSON file from dictionary
    #         with open(CLIENT_SECRET_FILE, 'w') as outfile:
    #             json.dump(client_secret_file, outfile)

    #     flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    #     flow.user_agent = APPLICATION_NAME
    #     credentials = tools.run_flow(flow, store)
    #     # print('Storing credentials to ' + credential_path)

    return credentials
