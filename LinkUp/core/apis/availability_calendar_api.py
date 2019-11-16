from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from ..models import Schedule
from .calendar_api import free_busy_month
from django.utils import timezone
from pytz import UTC
import json


def format_google_calendar_availability(user_id):
    """
    Takes the next thirty days of the user's google calendar data and puts it into a format compatible with the
    availability calendar template

    :param user_id: The id of the user we are formatting the availability calendar for
    :return: A dictionary keyed on string hours (12 AM, 12:30 AM, ..., 11:30 PM) with values that are lists of booleans
            each representing a day of the month for which the user is busy on the keyed time, or is not (True if busy)

            {
                '12:00 AM': [False] * 30
                ...
                '10:00 AM': [False, False, False, ..., True, True, ..., False]
            }
    """
    user = User.objects.get(id=user_id)
    fb = free_busy_month(user)

    today = timezone.localtime(datetime.utcnow().replace(tzinfo=UTC))

    busy_times = {}
    for half_hour_periods in range(48):
        busy_times[half_hour_periods] = [False] * 30

    fb_converted = convert_to_local_time(fb)

    for times in fb_converted:
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


def convert_to_local_time(fb):
    """
    Converts to local time and splits up busy periods over multiple dates
    """
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
        return None

    users_availability_string = schedule_query[0].availability

    # Decode the availability
    users_availability = json.loads(users_availability_string)
    for time_range in users_availability:
        for time in time_range.keys():
            time_range[time] = parse_datetime(time_range[time]).replace(tzinfo=UTC)

    return users_availability


def json_datetime_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, ...):
        return ...
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))