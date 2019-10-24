from django.shortcuts import render


def home(request):
	return render(request, "core/homepage.html", {})


def event_page(request):
	return render(request, "core/event_page.html", {})
