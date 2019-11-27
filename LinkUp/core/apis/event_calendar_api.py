from .availability_calendar_api import format_event_availability_calendar
from ..models import Event
from datetime import datetime, timedelta

def format_group_availability_calendar(event_id) :
    """
    Takes in event_id, accesses all user's event availability in database, converts to the viewing user's timezone,
    and finally creates a table of the possible days and hours of the event with the each cell representing the number
    of event members available at that given time.

    :param event_id:
    :return: a table of integers keyed on times
        "13:00" [8, 10, 9, 10, ....]
        "13:30" [9, 9, 8, ....]
    """
    #First access and store all user_id
    query = Event.objects.filter(event_id=event_id)
    if query.count() == 0 :
        return None
    else :
        event = query[0]

    user_schedules = []
    for user in event.members.all() :
         user_schedules.append({user: format_event_availability_calendar(user, event_id)})

    #Create appropriate table for group_availability
    group_availability = {}
    number_of_days = (event.potential_end_date - event.potential_start_date).days + 1
    dt = datetime(year=1, month=1, day=1)
    dt_end = datetime(year=1, month=1, day=2)
    while dt < dt_end :
        group_availability[dt.strftime("%I:%M %p")] = [[] for i in range(number_of_days)]
        dt = dt + timedelta(minutes=30)



    #Properly fill in dictionary with users availabile at each time
    for schedule in user_schedules :
        schedule_user = list(schedule.keys())[0]
        availability = list(schedule.values())[0]
        for half_hour_period in availability :
            day_tracker = 0
            for day in availability[half_hour_period] :
                if day is False :
                    group_availability[half_hour_period][day_tracker].append(schedule_user)
                day_tracker = day_tracker + 1

    return group_availability

