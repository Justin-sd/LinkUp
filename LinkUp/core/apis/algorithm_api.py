from ..models import *
from .availability_calendar_api import *
from .calendar_api import *
import json
from datetime import datetime, timedelta


def get_best(event_id):
    event_set = Event.objects.filter(event_id=event_id)

    event = event_set[0]
    # make the queryset of users into a list of users
    users = list(event.members.all())

    # make all these in minutes
    duration = int(event.duration)

    st = event.potential_start_date
    # round up the potential starting minutes
    if st.minute > 30:
        new_st = st.replace(minute=0)
        new_st =  new_st + timedelta(hours=1)
    elif st.minute > 0:
        new_st = st.replace(minute=30)
    elif st.minute == 0 or st.minute == 30:
        new_st = st
    start = convert_to_minutes(new_st, new_st)

    et = event.potential_end_date
    # round down potential ending minutes
    if et.minute > 30:
        new_et = et.replace(minute=30)
    elif et.minute > 0:
        new_et = et.replace(minute=0)
    elif et.minute == 0 or et.minute == 30:
        new_et = et
    end = convert_to_minutes(new_et, new_st)

    # Dictionary: starting times as keys and values is list of people who can make it,
    # keys incremented by duration
    optimal_times = {}
    # from start to end time, add keys of 30 minute increments with querysets of every user attending
    for i in range(start,end+1, duration):
        if i + duration > end:
            break
        optimal_times[i] = users.copy()

    all_user_times = []

    # have a list of all users times
    for u in users:
        # user_sched = free_busy_month(u)
        # schedule = json.dumps(user_sched, default=json_datetime_handler)

        # Schedule.objects.create(user=u, availability=schedule)

        # get user's schedules in datetime format
        for times in get_users_saved_schedule(u):
            start_time = list(times.values())[0]
            # round DOWN the starting minutes
            if start_time.minute > 30:
                starting = start_time.replace(minute=30)
            elif start_time.minute > 0:
                starting = start_time.replace(minute=0)
            elif start_time.minute == 0 or start_time.minute == 30:
                starting = start_time
            the_start = convert_to_minutes(starting, new_st)

            end_time = list(times.values())[1]
            # round UP the ending minutes
            if et.minute > 30:
                ending = et.replace(minute=0)
                ending = ending + timedelta(hours=1)
            elif et.minute > 0:
                ending = et.replace(minute=30)
            elif et.minute == 0 or et.minute == 30:
                ending = end_time
            the_end = convert_to_minutes(ending, new_st)

            # try to find the keys in 30 minute increments and remove the user
            # from the corresponding list
            for i in range(the_start, the_end+1, 30):
                if i in optimal_times:
                    dict_value = optimal_times.get(i)
                    if u in dict_value:
                        dict_value.remove(u)
                    new_dict = {i: dict_value}
                    optimal_times.update(new_dict)

    # go through the optimal times and find which list contains
    # most users then append to new list
    curr_max = len(list(optimal_times.values())[0])
    append_list = []
    for times in optimal_times:
        if len(optimal_times[times]) >= curr_max:
            # append a list of pairs, first = datetime of start second = list of attending
            # with the ending of the list having more people available
            append_list.append((convert_to_datetime(new_st, times), optimal_times.get(times)))
            curr_max = len(optimal_times[times])

    # return the reversed list
    return append_list[::-1]


# convert a datetime to minutes elapsed
def convert_to_minutes(time, starting):
    elapsed = time - starting
    minutes = int(elapsed.total_seconds()/60)
    return minutes

# convert minutes to a datetime by getting starting datetime and timedelta by minutes
def convert_to_datetime(starting, mins):
    time = starting + timedelta(minutes=mins)
    return time