from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from ..models import Schedule
from .calendar_api import free_busy_month, get_users_preferred_timezone
from django.utils import timezone
from pytz import UTC, timezone as pytz_timezone
from django.utils.dateparse import parse_datetime
import json

from ..models import Event, Schedule, EventSchedule, UserTimezone
from .calendar_api import free_busy_month


def format_google_calendar_availability(user):
    """
    Takes the next thirty days of the user's google calendar data and puts it into a format compatible with the
    availability calendar template

    :param user: The user we are formatting the google availability calendar for
    :return: A dictionary keyed on string hours (12 AM, 12:30 AM, ..., 11:30 PM) with values that are lists of booleans
            each representing a day of the month for which the user is busy on the keyed time, or is not (True if busy)

            {
                '12:00 AM': [False] * 30
                ...
                '10:00 AM': [False, False, False, ..., True, True, ..., False]
            }
    """
    fb = free_busy_month(user)
    number_of_days = 30  # About one month of google calendar data
    start_date = timezone.localtime(datetime.utcnow().replace(tzinfo=UTC))
    availability = convert_to_local_time(fb, user)

    return format_availabilities(availability, start_date, number_of_days)


def format_general_availability_calendar(user):
    """
    Formats the users general availability calendar, which works as a starting point for all their new event
    availabilities

    :param user: The user we are formatting the general availability calendar for
    :return: A dictionary keyed on string hours (12 AM, 12:30 AM, ..., 11:30 PM) with values that are lists of booleans
            each representing a day of the month for which the user is busy on the keyed time, or is not (True if busy)

            {
                '12:00 AM': [False] * 30
                ...
                '10:00 AM': [False, False, False, ..., True, True, ..., False]
            }
    """
    fb = get_users_saved_schedule(user)
    number_of_days = 30  # Support one month of general availability for now
    start_date = timezone.localtime(datetime.utcnow().replace(tzinfo=UTC))
    availability = convert_to_local_time(fb, user)

    return format_availabilities(availability, start_date, number_of_days)


def format_event_availability_calendar(user, event_id):
    """
    Formats the availability calendar for the user and a specific event the user is in

    :return: A dictionary keyed on string hours (12 AM, 12:30 AM, ..., 11:30 PM) with values that are lists of booleans
            each representing a day of the month for which the user is busy on the keyed time, or is not (True if busy)
            {
                '12:00 AM': [False] * 30
                ...
                '10:00 AM': [False, False, False, ..., True, True, ..., False]
            }
    """
    event = Event.objects.get(event_id=event_id)
    availability = get_users_event_schedule(user, event)
    availability = convert_to_local_time(availability, user)

    # Filter out availability dates that are not part of the event
    start_date = timezone.localtime(event.potential_start_date)
    end_date = timezone.localtime(event.potential_end_date)
    availability = filter_availability(availability, start_date, end_date)
    number_of_days = (end_date - start_date).days + 1

    return format_availabilities(availability, start_date, number_of_days)


def format_availabilities(availability, start_date, number_of_days):
    """
    Handles the formatting of all availability calendars
    :param availability:    A list of dictionary objects containing start and end times representing time ranges in which
                            the user is busy
    :param start_date:      The first day for which availability is displayed
    :param number_of_days:  The number of days we are showing availability for

    :return: A dictionary keyed on string hours (12 AM, 12:30 AM, ..., 11:30 PM) with values that are lists of booleans
            each representing a day of the month for which the user is busy on the keyed time, or is not (True if busy)
            {
                '12:00 AM': [False] * 30
                ...
                '10:00 AM': [False, False, False, ..., True, True, ..., False]
            }

    """
    busy_times = {}
    for half_hour_periods in range(48):
        busy_times[half_hour_periods] = [False] * number_of_days

    for times in availability:
        start = timezone.localtime(times["start"])
        end = timezone.localtime(times["end"])
        index = start.hour * 2
        if start.minute >= 30:
            index += 1

        while start < end:
            busy_times[index][(start.day - start_date.day)] = True
            index += 1
            start = start + timedelta(minutes=30)

    # Change dictionary keys to dates
    result = {}
    dt = datetime(year=1, month=1, day=1)
    for half_hour_period in range(48):
        result[dt.strftime("%I:%M %p")] = busy_times[half_hour_period]
        dt = dt + timedelta(minutes=30)

    return result


def convert_to_local_time(fb, user):
    """
    Converts to local time and splits up busy periods over multiple dates
    :param: fb:     The list of free busy dictionaries containing datetimes in UTC time
    :param: user:   The user whose timezone we are converting to. This timezone is taken from their google calendar.
                    Maybe it would be better to calculate it from their browser using javascript?
    """
    # Must do this for timezone.localtime to work!
    # Set users timezone
    activate_users_saved_timezone(user)

    split_fb = []
    for times in fb:
        start = timezone.localtime(times["start"])
        end = timezone.localtime(times["end"])

        while start.day != end.day:
            dt_halfway = datetime.combine(start, datetime.max.time()).replace(tzinfo=end.tzinfo)
            split_time = {"start": start, "end": timezone.localtime(dt_halfway)}
            split_fb.append(split_time)
            start = datetime.combine(start + timedelta(days=1), datetime.min.time()).replace(tzinfo=end.tzinfo)

        split_fb.append({"start": start, "end": end})
    return split_fb


def get_list_of_next_n_days(num_days):
    """
    :return: A list of datetime objects from today to thirty days from now (exclusive)
    :param num_days: The number of date objects to return in the list
    """
    dates = []

    today = datetime.utcnow().replace(tzinfo=UTC)
    next_month = today + timedelta(days=num_days)
    while today < next_month:
        dates.append(timezone.localtime(today))
        today = today + timedelta(days=1)

    return dates


def get_users_saved_schedule(user):
    """
    :param user: The users whose availability is being returned
    :return: The users availability converted into standard format:

                [{'start': datetime(..., hour=4, minute=30), 'end': datetime(..., hour=6, minute=30)}, ...]
    """
    schedule_query = Schedule.objects.filter(user=user)
    if schedule_query.count() == 0:
        users_availability_string = "[]"
    else:
        users_availability_string = schedule_query[0].availability
    return decode_availability(users_availability_string)


def get_users_event_schedule(user, event):
    """
    :param user: The user whose event schedule we are retrieving
    :param event: The event the user is in
    :return: The users corresponding schedule for the event with the given event_id
    """
    event_schedule_query = EventSchedule.objects.filter(user=user, event=event)
    if event_schedule_query.count() == 0:
        general_schedule = get_users_saved_schedule(user=user)
        availability = json.dumps(general_schedule, default=json_datetime_handler)
        EventSchedule.objects.create(user=user, event=event, availability=availability)
        return general_schedule
    return decode_availability(event_schedule_query[0].availability)


def decode_availability(availability):
    """
    :param availability: Stringified availability
    :return: The users availability converted into standard format:

                [{'start': datetime(..., hour=4, minute=30), 'end': datetime(..., hour=6, minute=30)}, ...]
    """
    users_availability = json.loads(availability)
    for time_range in users_availability:
        for time in time_range.keys():
            time_range[time] = timezone.localtime(parse_datetime(time_range[time]).replace(tzinfo=UTC))

    return users_availability


def filter_availability(availability, start_date, end_date):
    """
    Removes dates that are not in the range of start_date.day to end_date.day
    """
    filtered_availability = []
    for time_range in availability:
        if time_range["start"].day < start_date.day:
            continue
        if time_range["end"].day <= end_date.day:
            filtered_availability.append(time_range)

    return filtered_availability


def get_event_availability_dates(event_id):
    """
    :param event_id: The event
    :return: A list of potential event days
    """
    event = Event.objects.get(event_id=event_id)
    start_date = timezone.localtime(event.potential_start_date)
    end_date = timezone.localtime(event.potential_end_date)
    possible_dates = []
    dt = datetime(year=1, month=start_date.month, day=start_date.day)
    while dt.day <= end_date.day:
        possible_dates.append(dt)
        dt = dt + timedelta(days=1)

    return possible_dates


def activate_users_saved_timezone(user):
    """
    Activates the timezone that the users browser supplies
    :param user: The user whose timezone we are using to set the timezones
    :return: None
    """
    try:
        timezone.activate(UserTimezone.objects.get(user=user).timezone_str)

    except ObjectDoesNotExist:
        # If we can't find it, just make it LA for now
        timezone.activate('America/Los_Angeles')


def json_datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, ...):
        return ...
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))

def convert_user_calendar_to_normal(calendar, user) :
    """
    :param calendar: The formatted calendar given in JS
    :return: The users availability converted into standard format:
            [{'start': datetime(..., hour=4, minute=30), 'end': datetime(..., hour=6, minute=30)}, ...]
    """
    new_calendar = json.load(calendar)
    local_tz = pytz_timezone(get_users_preferred_timezone(user))
    converted_calendar = []
    for hours in new_calendar :
        i = 0
        for day in new_calendar[hours] :
            today =(datetime.now() + timedelta(days=i))
            hour = hours.split('-')

            if day is True :
                #add .replace(tzinfo=UTC)
                converted_calendar.append({'start': datetime(today.year, today.month, today.day, int(hour[0]), int(hour[1]), tzinfo=local_tz).replace(tzinfo=UTC),
                                             'end': datetime(today.year, today.month, today.day, int(hour[0]) + 1, int(hour[1]), tzinfo=local_tz).replace(tzinfo=UTC) })
            i = i + 1

    #Need to simplify events


    return json.dumps(converted_calendar, default=json_datetime_handler)

def convert_stored_calendar_to_UI(user_id) :
    user = User.objects.get(id=user_id)
    schedule = get_users_saved_schedule(user)
    if schedule is None :
        return format_google_calendar_availability(user_id)

    today = timezone.localtime(datetime.utcnow().replace(tzinfo=UTC))
    busy_times = {}
    for half_hour_periods in range(48):
        busy_times[half_hour_periods] = [False] * 30

    #converted_schedule = convert_to_local_time(schedule)
    converted_schedule = schedule

    for times in converted_schedule :
        start = timezone.localtime(times["start"])
        end = timezone.localtime(times["end"])
        index = start.hour * 2
        if start.minute >= 30:
            index += 1

        while start < end:
            busy_times[index][(start.day - today.day)] = True
            index += 1
            start = start + timedelta(minutes=30)

    # Change dictionary keys to dates
    result = {}
    dt = datetime(year=1, month=1, day=1)
    for half_hour_period in range(48):
        result[dt.strftime("%I:%M %p")] = busy_times[half_hour_period]
        dt = dt + timedelta(minutes=30)

    return result
