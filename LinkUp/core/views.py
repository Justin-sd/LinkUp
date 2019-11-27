from django.shortcuts import render, redirect

from .apis import availability_calendar_api, sendEmail_api, algorithm_api, contact_us_api, event_calendar_api
from .models import Event, Schedule, UserTimezone
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
import uuid
from datetime import datetime


@login_required()
def home(request):
    user = request.user
    user_events = Event.objects.filter(members=user)
    no_user_events = False
    if user_events.count() is 0:
        no_user_events = True

    context = {
        "user_events": user_events,
        "no_user_events": no_user_events,
    }
    return render(request, "core/homepage.html", context)


@login_required()
def event_page(request, event_id):
    event_query_set = Event.objects.filter(event_id=event_id)

    if event_query_set.count() != 1:
        return render(request, "core/error_page", {})
    # User Object
    user = request.user

    # Event Objects
    event = event_query_set[0]
    user_events = Event.objects.filter(members=user)

    if user in event.members.all():
        new_user = False
    else:
        new_user = True

    if user in event.admins.all():
        admin = True
    else:
        admin = False

    # Get the users event schedule
    busy_times = availability_calendar_api.format_event_availability_calendar(user, event_id)
    available_dates = availability_calendar_api.get_event_availability_dates(event_id)
    time_list = algorithm_api.get_best(event_id)
    group_availability = event_calendar_api.format_group_availability_calendar(event_id)
    member_count = event.members.count()

    context = {"event": event, "admin": admin, "user": user, 'busy_times': busy_times,
               "availability_dates": available_dates, "time_list": time_list, "user_events": user_events,
               "event_id": event_id, "group_availability": group_availability, "member_count": member_count, "create_event_form": EventForm(), "new_user": new_user}
    return render(request, "core/event_page.html", context)


@login_required()
def my_events(request):
    user = request.user

    user_name = user.username
    user_events = Event.objects.filter(members=user)
    user_event_count = user_events.count()

    busy_times = availability_calendar_api.format_general_availability_calendar(request.user)
    availability_dates = availability_calendar_api.get_list_of_next_n_days(30)

    context = {
        "user_events": user_events,
        "user_name": user_name,
        "user_event_count": user_event_count,
        "busy_times": busy_times,
        "availability_dates": availability_dates,
        "create_event_form": EventForm(),
    }

    return render(request, "core/my_events.html", context)


@login_required()
def my_availability(request):
    user = request.user
    user_events = Event.objects.filter(members=user)
    # Load users general availability from database
    busy_times = availability_calendar_api.format_general_availability_calendar(request.user)
    availability_dates = availability_calendar_api.get_list_of_next_n_days(30)

    context = {"user_events": user_events, "busy_times": busy_times, "availability_dates": availability_dates}
    return render(request, "core/my_availability.html", context)


@login_required()
def import_google_calendar_data(request):
    busy_times = availability_calendar_api.format_google_calendar_availability(request.user)
    availability_dates = availability_calendar_api.get_list_of_next_n_days(30)

    context = {"busy_times": busy_times, "availability_dates": availability_dates}
    return render(request, "core/my_availability.html", context)


@login_required()
def attendees_page(request):
    return render(request, "core/attendees.html", {})


def login_page(request):
    return render(request, "core/login_page.html", {})


def contact(request):
    return render(request, "core/contact.html", {})


def donate(request):
    return render(request, "core/donate.html", {})


def about(request):
    return render(request, "core/about.html", {})


def save_availability(request):
    # Get user and local timezone
    user = request.user
    new_availability_dates = availability_calendar_api.convert_user_calendar_to_normal(request, user)

    query = Schedule.objects.filter(user=user)
    if query.count() == 0:
        Schedule.objects.create(availability=new_availability_dates, user=user)
    else:
        schedule = query[0]
        schedule.availability = new_availability_dates
        schedule.save()

    return render(request, "core/availability_calendar.html", {})


def createUser(request):
    if request.method == "POST":
        user = User.objects.create_user(first_name=request.POST.get("first_name"),
                                        last_name=request.POST.get("last_name"),
                                        email=request.POST.get("email"),
                                        password=request.POST.get("password"),
                                        username=request.POST.get("email"))
        user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        login(request, user)
    return render(request, "core/homepage.html", {})


def login_user(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.method == "POST":
        try:
            user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('homepage/')
        else:
            return render(request, "core/failed_login.html", {})


def failed_login(request):
    return render(request, "core/failed_login.html", {})


def send_email(request):
    data = request.POST
    invitee_email = data["invitee_email"]
    event_id = data["event_id"]
    event_url = "https//:LinkUp.com/event_page/" + event_id
    sendEmail_api.send_invite_email(event_url, invitee_email)
    return HttpResponse("Success")


def send_contact(request):
    contact_us_api.send_contact_email(name, message, email)


def get_create_event_form(request):
    # If POST request, process the form
    if request.method == 'POST':
        form = EventForm(request.POST)
        # If form is valid, save the event
        if form.is_valid():
            event_id = str(uuid.uuid1())
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            duration = form.cleaned_data["duration"]
            start = form.cleaned_data["potential_start_date"]
            end = form.cleaned_data["potential_end_date"]
            no_earlier_than = form.cleaned_data["no_earlier_than"]
            no_later_than = form.cleaned_data["no_later_than"]
            new_event = Event.objects.create(event_id=event_id, title=title, description=description, duration=duration,
                                             owner=request.user, potential_start_date=start, potential_end_date=end,
                                             no_earlier_than=no_earlier_than, no_later_than=no_later_than)
            new_event.members.add(request.user)
            new_event.admins.add(request.user)
            return redirect('/event_page/' + event_id)
        else:
            return HttpResponse(status=500)
    else:
        # If GET request, render the form
        form = EventForm()
        return render(request, 'core/create_event_modal.html', {'create_event_form': form})


def join_event(request, event_id):
    event_query_set = Event.objects.filter(event_id=event_id)
    event = event_query_set[0]
    event.members.add(request.user)
    return event_page(request, event_id)



@login_required()
def my_account(request):
    return render(request, "core/my_account.html", {})


@login_required()
def privacy_policy(request):
    return render(request, "core/privacy_policy.html", {})


def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/my_account/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/password_change.html', {
        'form': form
    })


def logout_user(request):
    """
    Log the user out
    """
    logout(request)
    return render(request, "core/homepage.html", {})


def update_timezone(request):
    """
    :param: request: Request contains POST data containing time zone from the user's browser
    Update the users timezone by detecting it from the browser so we can display time ranges in their timezone
    """
    user_timezone = request.POST.get("time_zone")
    user = request.user
    query = UserTimezone.objects.filter(user=user)
    if query.count() != 0:
        query.update(user=user, timezone_str=user_timezone)
    else:
        UserTimezone.objects.create(user=user, timezone_str=user_timezone)
    return HttpResponse("Success")


def change_event_title(request):
    if request.method == 'POST':
        event = Event.objects.filter(event_id=request.POST.get('event_id'))
        event.update(title=request.POST.get('new_title'))
    return HttpResponse("Success")


def change_event_description(request):
    if request.method == 'POST':
        event = Event.objects.filter(event_id=request.POST.get('event_id'))
        event.update(description=request.POST.get('new_description'))
    return HttpResponse("Success")


def add_event_admin(request):
    if request.method == 'POST':
        event = Event.objects.filter(event_id=request.POST.get('event_id'))
        newadmin = User.objects.filter(username=request.POST.get('new_admin'))
        event[0].admins.add(newadmin[0])
    return HttpResponse("Success")
