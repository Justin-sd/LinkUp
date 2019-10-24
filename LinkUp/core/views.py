from django.shortcuts import render

# Create your views here.


def home(request):
	return render(request, "core/homepage.html", {})


def event_page(request):
	return render(request, "core/event_page.html", {})
