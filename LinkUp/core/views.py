from django.shortcuts import render, redirect
from .apis import availability_calendar_api, sendEmail_api, algorithm_api
from .models import Event, UserTimezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse


def home(request):
    return render(request, "core/homepage.html", {})


@login_required()
def event_page(request, event_id):
    for i in range(10000):
        event_query_set = Event.objects.filter(event_id=event_id)
        if event_query_set.count() == 1 and event_query_set[0].admins.count() >= 1:
            break

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

    # Get the users event schedule
    busy_times = availability_calendar_api.format_event_availability_calendar(user, event_id)
    available_dates = availability_calendar_api.get_event_availability_dates(event_id)
    time_list = algorithm_api.get_best(event_id)

    context = {"event": event, "admin": admin, "user": user, 'busy_times': busy_times,
               "availability_dates": available_dates, "time_list": time_list}
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
        "availability_dates": availability_dates
    }

    return render(request, "core/my_events.html", context)


@login_required()
def my_availability(request):
    # Load users general availability from database
    busy_times = availability_calendar_api.format_general_availability_calendar(request.user)
    availability_dates = availability_calendar_api.get_list_of_next_n_days(30)

    context = {"busy_times": busy_times, "availability_dates": availability_dates}
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
        user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        user.is_active = True
        login(request, user, backend)
    return render(request, "core/homepage.html", {})


def send_email(request):
    data = request.POST
    print(data)
    invitee_email = data["invitee_email"]
    event_id = data["event_id"]
    event_url = "https//:LinkUp.com/event_page/" + event_id
    sendEmail_api.send_invite_email(event_url, invitee_email)
    return HttpResponse("Success")


def send_contact(request):
    send_contact_email(name, message, email)


def eventcreation(request, idd, title, description, start,
                  end, duration):
    userr = request.user
    event = Event.objects.create(event_id=idd, title=title,
                                 description=description,
                                 owner=userr, potential_start_date=start,
                                 potential_end_date=end, duration=int(duration))
    event.admins.add(userr)  # creator is admin
    event.members.add(userr)  # creator is also a member
    return event_page(request, event.event_id)


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
    UserTimezone.objects.update(user=user, timezone_str=user_timezone)
    return HttpResponse("Success")
