# Google Calendar CSV Event Importer
This script automatically creates google calendar events based on spreadsheet file

### Features:
- OAuth2 authentication with Gmail
- Token storage and refresh
- Read the multiple events from a CSV file
- Usage via command line

---

### Requirements
- Google cloud console set up
- Install required libraries
  - google-auth
  - google-auth-oauthlib
  - google-api-python-client
- Google API credentials (client_secret.json file)

### Google cloud
  - Go to https://console.cloud.google.com/
  - Create a new project
  - Activate google calendar api
  - Necessary scope: googleapis.com/auth/calendar
  - Create OAuth 2.0 Client ID credentials
  - Download the .json and place it in the project folder
  - Account used must be added as a beta tester for unpublished projects

### CSV file
- Contains all events which will be created
- Must contain these headers:
  - summary
  - description
  - location
  - start
  - end
  - colorId

### Date and Time Format

- Dates must follow the ISO 8601 format:

```YYYY-MM-DDTHH:MM:SS±HH:MM```

Example: 2025-04-01T08:00:00-03:00 (April 1st, 2025, 08:00 AM in the -3:00 timezone).

---

 ### Running
```bash python Scheduler.py events.csv```

First use will open a browser window for Google authentication. Afterward, a token is saved in token.pickle for reuse

