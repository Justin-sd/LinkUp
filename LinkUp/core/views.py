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


def my_events(request, user_name):
	all_events = Event.objects.all()
	number_of_events = Event.objects.count()

	if number_of_events < 1:
		return render(request, "core/error_page", {})

	context = {"all_events": all_events, "user_name": user_name, "number_of_events": number_of_events}
	return render(request, "core/my_events.html", context)


def attendees_page(request):
	return render(request, "core/attendees.html", {})