import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#google cloud console scopes and login
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.pickle"
CLIENT_SECRET_FILE = "client_secret.json"

#Get credentials to login in google account
def get_credentials():
    credentials = None
    
    #Token for easier authentication
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)

    #Refresh token
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        #First execution
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        #saves newest token
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return credentials

def main():
    cred = get_credentials()
    service = build("calendar", "v3", credentials=cred)
    event = input("Type event name: ")
    desc = input("Type event description: ")

if __name__ == "__main__":
    main()