from __future__ import print_function
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from pytz import timezone as pytz_timezone

# Production API stuff
from apiclient import discovery
import httplib2
from oauth2client import client

# API testing stuff
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
CLIENT_SECRET_FILE = 'core/apis/credentials.json'


def exchange_auth_code_for_calendar_service(auth_code):
    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        SCOPES,
        auth_code)

    http_auth = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http_auth)


# Will not work with deployed system, for testing only
def get_service(user):
    """
    Creates service for google calendar API. Attempts to load credentials from file storage,
    but will remake credentials if they do not exist or are invalid.

    :param user: Django User object for the user whose calendar is being accessed
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('core/apis/tokens/' + str(user.id)):
        with open('core/apis/tokens/' + str(user.id), 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'core/apis/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('core/apis/tokens/' + str(user.id), 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_users_preferred_timezone(user, service):
    """
    Determines the users preferred timezone by checking what timezone they use for their primary google calendar

    :param user: Django User object for the user whose calendar is being accessed
    :return: A string representation of the timezone:

        - "Etc/GMT+8"
    """
    primary_calendar = service.calendarList().get(calendarId='primary').execute()

    return primary_calendar['timeZone']


def get_calendar_id_list(user, service):
    """
    :param user: Django User object for the user whose calendar is being accessed
    :return: A list of all the users calendar IDs
    """
    calendars = service.calendarList().list().execute()["items"]
    # If the user has a ton of calendars, there may be a second page to the
    # query in calendars["nextPageToken"]. People with this many calendars do
    # not deserve a scheduling app, however.

    return [calendar["id"] for calendar in calendars]


def free_busy_month(user, service):
    """
    :param user: Django User object for the user whose calendar is being accessed

    Finds all the periods in all the users google calendars in which the user is BUSY
    :return: A list of dictionaries with keys 'start' and 'end' that are datetimes representing a range of time where
             the user is busy on any of their google calendars:

                [{'start': datetime(..., hour=4, minute=30), 'end': datetime(..., hour=6, minute=30)}, ...]

    """
    min_time = datetime.combine(datetime.utcnow(), datetime.min.time())
    max_time = min_time + timedelta(days=30)

    min_time = min_time.isoformat() + 'Z'  # 'Z' indicates UTC time
    max_time = max_time.isoformat() + 'Z'  # 'Z' indicates UTC time

    body = {"items": [], "timeMin": min_time, "timeMax": max_time}
    # body also needs to specify which calendar ids, we want them all. This is the format it needs:
    #   "items": [  # List of calendars and/or groups to query.
    #         {
    #             "id": "A String",  # The identifier of a calendar or a group.
    #         },
    #   ]
    calendar_ids = get_calendar_id_list(user, service)
    for calendar_id in calendar_ids:
        body["items"].append({"id": calendar_id})

    free_busy_result_calendars = service.freebusy().query(body=body).execute()['calendars']

    result = []
    for cal in free_busy_result_calendars.values():
        for times in cal['busy']:
            dt_start = parse_datetime(times["start"])
            dt_end = parse_datetime(times["end"])
            result.append({'start': dt_start, 'end': dt_end})

    preferred_timezone = get_users_preferred_timezone(user, service)
    timezone.activate(preferred_timezone)
    return result


def add_event(user, service, start_time, end_time, event_title, event_description=None):
    """
    Adds a new event to the users primary calendar

    :param user: Django User object for the user whose calendar is being accessed
    :param start_time: datetime object for the start of the event
    :param end_time: datetime object for the end of the event
    :param event_title: The title of the event
    :param event_description: An optional description of the event
    :return: True if event created successfully, False otherwise
    """
    body = {"start": {"dateTime": start_time.isoformat() + 'Z'},
            "end": {"dateTime": end_time.isoformat() + 'Z'},
            "summary": event_title,
            "description": event_description}
    try:
        service.events().insert(calendarId="primary", body=body).execute()
    except:
        return False
    return True
