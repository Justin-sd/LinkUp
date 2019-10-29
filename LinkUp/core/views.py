from django.shortcuts import render
from .models import Event


def home(request):
	return render(request, "core/homepage.html", {})


def event_page(request, event_id):
	id_name = event_id
	event_query_set = Event.objects.filter(event_id=event_id)
	if event_query_set.count() != 1:
		return render(request, "core/error_page", {})

	event = event_query_set[0]

	event_title = event.title
	event_description = event.description

	context = {"event_title": event_title, "event_description": event_description}
	return render(request, "core/event_page.html", context)


def my_events(request):
	user = request.user

	user_name = user.first_name
	users_events = Event.objects.filter(owner=user)
	user_event_count = users_events.count()

	context = {"users_events": users_events, "user_name": user_name, "user_event_count": user_event_count}
	return render(request, "core/my_events.html", context)


def attendees_page(request):
	return render(request, "core/attendees.html", {})


def login_page(request):
	return render(request, "core/login_page.html", {})
