from django.shortcuts import render
from .apis import availability_calendar_api
from .models import Event
from .apis import availability_calendar_api
from .apis import calendar_api
from .apis import sendEmail_api
from django.contrib.auth.decorators import login_required
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .apis import contact_us_api


def home(request):
    return render(request, "core/homepage.html", {})


@login_required()
def event_page(request, event_id):
    event_query_set = Event.objects.filter(event_id=event_id)
    if event_query_set.count() != 1:
        return render(request, "core/error_page", {})

    # Event Objects
    event = event_query_set[0]

    # User Object
    user = request.user

    if user in event.admins.all():
        admin = True
    else:
        admin = False

    context = {"event": event, "admin": admin, "user": user}
    return render(request, "core/event_page.html", context)


@login_required()
def my_events(request):
    user = request.user

    user_name = user.username
    user_events = Event.objects.filter(members=user)
    user_event_count = user_events.count()

    busy_times = availability_calendar_api.format_google_calendar_availability(request.user.id)
    availability_dates = availability_calendar_api.get_list_of_next_n_days(30)

    context = {
        "user_events": user_events,
        "user_name": user_name,
        "user_event_count": user_event_count,
        "busy_times": busy_times,
        "availability_dates": availability_dates
    }

    return render(request, "core/my_events.html", context)


@login_required()
def my_availability(request):
    # Load busy times from database
    busy_times = availability_calendar_api.format_google_calendar_availability(request.user.id)
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

def login_user(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        login(request, user)
    return render(request, "core/homepage.html", {})


def send_email(request):
	sendEmail_api.send_invite_email(invite_link, [invite_email])
	return render(request, "core/homepage.html", {})

def send_contact(request):
    send_contact_email(name, message, email)