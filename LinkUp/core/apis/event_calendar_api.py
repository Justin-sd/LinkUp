from django.utils import timezone
from pytz import UTC
from .availability_calendar_api import format_event_availability_calendar, activate_users_saved_timezone
from ..models import Event
from datetime import datetime, timedelta


def format_group_availability_calendar(event_id):
    """
    Takes in event_id, accesses all user's event availability in database, converts to the viewing user's timezone,
    and finally creates a table of the possible days and hours of the event with the each cell representing the number
    of event members available at that given time.

    :param event_id:
    :return: a table of integers keyed on times
        "13:00" [8, 10, 9, 10, ....]
        "13:30" [9, 9, 8, ....]
    """
    # First access and store all user_id
    query = Event.objects.filter(event_id=event_id)
    if query.count() == 0:
        return None
    else:
        event = query[0]

    user_schedules = []
    for user in event.members.all():
        user_schedules.append({user: format_event_availability_calendar(user, event_id)})

    # Create appropriate table for group_availability
    group_availability = {}
    number_of_days = (event.potential_end_date - event.potential_start_date).days + 1
    dt = datetime(year=1, month=1, day=1)
    dt_end = datetime(year=1, month=1, day=2)
    while dt < dt_end:
        group_availability[dt.strftime("%I:%M %p")] = [[] for i in range(number_of_days)]
        dt = dt + timedelta(minutes=30)

    # Properly fill in dictionary with users available at each time
    for schedule in user_schedules:
        schedule_user = list(schedule.keys())[0]
        availability = list(schedule.values())[0]
        for half_hour_period in availability:
            day_tracker = 0
            for day in availability[half_hour_period]:
                if day is False:
                    group_availability[half_hour_period][day_tracker].append(schedule_user)
                day_tracker = day_tracker + 1

    return group_availability


def add_member_ratios(event_id, group_availability):
    """
    :param event_id: The id of the event
    :param group_availability: The formatted group availability calendar
    :return:
    """
    # First access and store all user_id
    query = Event.objects.filter(event_id=event_id)
    if query.count() == 0:
        return None
    else:
        event = query[0]

    # Create appropriate table for group_availability
    group_ratio = {}
    number_of_days = (event.potential_end_date - event.potential_start_date).days + 1
    dt = datetime(year=1, month=1, day=1)
    dt_end = datetime(year=1, month=1, day=2)
    while dt < dt_end:
        group_ratio[dt.strftime("%I:%M %p")] = [0.0] * number_of_days
        dt = dt + timedelta(minutes=30)

    # Fill in each related cell with the appropriate ratio of people available
    for half_hour_period in group_availability:
        day_tracker = 0
        for day in group_availability[half_hour_period]:
            group_ratio[half_hour_period][day_tracker] = len(day) / event.members.count()
            day_tracker = day_tracker + 1

    return group_ratio


def apply_event_time_constraints(event, busy_times):
    start_idx = event.no_earlier_than.hour * 2
    end_idx = event.no_later_than.hour * 2
    time_keys = list(busy_times.keys())
    time_keys = time_keys[start_idx:end_idx]
    busy_times_cut = dict.fromkeys(time_keys)
    for k in time_keys:
        busy_times_cut[k] = busy_times[k]

    return busy_times_cut


def cut_user_availability_dates_to_match_event(user, event, busy_times):
    activate_users_saved_timezone(user)
    start_date = timezone.localtime(datetime.utcnow().replace(tzinfo=UTC)).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0).replace(tzinfo=UTC)
    timezone.activate('UTC')
    event_start_date = event.potential_start_date

    time_keys = list(busy_times.keys())
    while start_date > event_start_date:
        event_start_date = event_start_date + timedelta(days=1)
        for k in time_keys:
            busy_times[k] = [False] + busy_times[k]

    return busy_times
