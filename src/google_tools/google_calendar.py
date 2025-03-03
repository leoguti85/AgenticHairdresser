from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import datetime


# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
AWESOME_id = os.environ["GOOGLE_ID"]


def get_credentials():
    """Shows basic usage of the Google Calendar API.
    Lists the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "src/google_tools/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds


creds = get_credentials()
service = build("calendar", "v3", credentials=creds)


def get_free_slots(args):
    """
    Check google calendar to find free time slots in a given day
    Returns: Free time slots
    """

    for k, v in args.items():
        start_time = v

    # start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
    end_time = start_time.replace(hour=23, minute=59)

    # Convert to RFC3339 format (Google API requirement)
    time_min = start_time.isoformat() + "Z"
    time_max = end_time.isoformat() + "Z"

    # Call the FreeBusy API
    freebusy_query = {
        "timeMin": time_min,
        "timeMax": time_max,
        "timeZone": "Europe/Brussels",
        "items": [{"id": AWESOME_id}],
    }

    response = service.freebusy().query(body=freebusy_query).execute()

    # Extract busy slots
    busy_slots = response["calendars"][AWESOME_id]["busy"]

    # Define working hours (for example: 9 AM to 5 PM)
    working_start = start_time.replace(
        hour=8,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
    )
    working_end = start_time.replace(
        hour=17,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
    )

    # Calculate free slots
    free_slots = []
    current_time = working_start

    for slot in busy_slots:
        busy_start = datetime.datetime.fromisoformat(
            slot["start"]
        )  # Remove 'Z' and convert to datetime
        busy_end = datetime.datetime.fromisoformat(slot["end"])

        if current_time < busy_start:  # There is a gap before the busy slot
            free_slots.append((current_time, busy_start))

        current_time = max(
            current_time, busy_end
        )  # Move to the end of the current busy slot

    # Check if there is free time after the last event until the end of working hours
    if current_time < working_end:
        free_slots.append((current_time, working_end))

    # Print free slots
    res = ["Available Free Slots:"]
    for slot in free_slots:
        res.append(
            f"From {slot[0].strftime('%Y-%m-%d %H:%M')} to {slot[1].strftime('%Y-%m-%d %H:%M')}"
        )

    return ", ".join(res)


def get_busy_slots(start_time):
    end_time = start_time.replace(hour=23, minute=59)

    # Convert to RFC3339 format (Google API requirement)
    time_min = start_time.isoformat() + "Z"
    time_max = end_time.isoformat() + "Z"

    # Call the FreeBusy API
    freebusy_query = {
        "timeMin": time_min,
        "timeMax": time_max,
        "timeZone": "Europe/Brussels",
        "items": [{"id": AWESOME_id}],
    }

    response = service.freebusy().query(body=freebusy_query).execute()

    # Extract busy slots
    busy_slots = response["calendars"][AWESOME_id]["busy"]

    # Print free slots
    print("Busy Slots:")
    for slot in busy_slots:
        print(f"From {slot['start']} to {slot['end']}")


def create_event(args):
    end_date = datetime.datetime.strptime(
        args["insert_date"], "%Y-%m-%dT%H:%M:%S"
    ) + datetime.timedelta(seconds=args["duration"])
    event = {
        "summary": f"{args['service']} - {args['customer']}",
        "location": "AwesomeHairdresser, 800 Howard St., San Francisco",
        "description": f"{args['service']}, price: {args['price']}",
        "start": {
            "dateTime": args["insert_date"],
            "timeZone": "Europe/Brussels",
        },
        "end": {
            "dateTime": end_date.isoformat(),
            "timeZone": "Europe/Brussels",
        },
    }

    calendar_list = service.calendarList().list(pageToken=None).execute()

    created_event = service.events().insert(calendarId=AWESOME_id, body=event).execute()
    print(f"Created event: {created_event['id']}")


if __name__ == "__main__":
    # Checking all events on a day

    qd1 = datetime.datetime(2025, 2, 27, 0, 0, 0)

    # Check whether there is an event on a specific date
    # qd1 = datetime.datetime(2025,2,25, 2,30,0).isoformat() + 'Z'
    # qd2 = datetime.datetime(2025,2,25, 2,30,1).isoformat() + 'Z'

    # get_busy_slots(qd1)
    # get_free_slots({'start_date': '2025-02-27T00:00:00'})

    # iqd = datetime.datetime(2025,2,26, 17,0,0).isoformat()
    create_event(
        {
            "insert_date": "2025-02-27T14:30:00",
            "service": "haircut",
            "customer": "Leonardo",
            "price": "32",
        }
    )
