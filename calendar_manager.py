import os, caldav
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta


def get_google_credentials():
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return creds

def manage_calendar(date, google:bool = True, url:str = None, user:str = None, password:str = None):
    if google:
        creds = get_google_credentials()
        client = caldav.DAVClient(
            url="https://apidata.googleusercontent.com/caldav/v2/",
            headers={"Authorization": f"Bearer {creds.token}"}
        )
    else:
        if url == "":
            raise ValueError("No custom url provided in config")
        if user == "" or password == "":
            raise ValueError("No username or password provided in config")
        client = caldav.DAVClient(
            url=url,
            username=user,
            password=password
        )
    date = date.split("-")
    principal = client.principal()
    calendars = principal.calendars()
    calendar = calendars[0]
    start = datetime(int(date[0]), int(date[1]), int(date[2]), 0, 0)
    end = start + timedelta(days=1)
    events = calendar.search(start=start, end=end, event=True, expand=True)
    result = []
    for event in events:
        ic = event.icalendar_component
        result.append(str(ic.get("summary")))
        result.append(str(ic.get("dtstart").dt.strftime("%H:%M")))

    return result