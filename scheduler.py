import os
import sys
import pickle
import csv
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

#google cloud console scopes and login
SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_FILE = "token.pickle"
CLIENT_SECRET_FILE = "client_secret.json"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z" 
# Example format: "2025-04-01T08:00:00-03:00" first of april 2025 at 8h 0min and 0 secs on -3h timezone

#Get credentials to log in to google account
def getCredentials():
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

#opens csv file and gets rows
def getData(sheet):
    with open(sheet, 'r') as sheet:
        read = csv.DictReader(sheet)
        #data gets a list of dictionaries
        data = [row for row in read]
    return data

#Attempts create an event
def setEvent(ev,ser):
    print(f"Creating event: {ev['summary']}...")
    ser.events().insert(calendarId="primary", body=ev).execute()


def main(sheet):
    cred = getCredentials()
    #gets google calendar api service
    service = build("calendar", "v3", credentials=cred)
    events = getData(sheet)

    #each row correspons to an event
    for row in events:
        #sets event to correct format
        try:
            #validates time format and parces to datetime
            startTime = datetime.strptime(row["start"], DATE_FORMAT)
            endTime = datetime.strptime(row["end"], DATE_FORMAT)

            event = { 
                "summary":row["summary"],
                "description":row["description"],
                "location":row["location"],
                "start": {
                    "dateTime":startTime.isoformat()
                },
                "end": {
                    "dateTime":endTime.isoformat()
                },
                "colorId": row["colorId"]
            }
            #create event
            setEvent(event,service)

        except ValueError as e:
            print(f"invalid date time format - {e}")

        except Exception as e:
            print(f"Error creating event - {e}")


    print('\nCalendar updated!')
        

if __name__ == "__main__":
    #checks presence of a spreadsheet file
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} [sheet.csv]")
    else:
        main(sys.argv[1])