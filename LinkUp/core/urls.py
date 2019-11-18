"""LinkUp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('contact/', views.contact),
    path('donate/', views.donate),
    # availability
    path('my_availability/', views.my_availability),
    path('my_availability/google_calendar/', views.import_google_calendar_data),
    # Users
    path('create_user/', views.createUser),
    path('login_page/', TemplateView.as_view(template_name="core/login_page.html")),
    path('login_user/', views.login_user),
    path('accounts/logout', TemplateView.as_view()),
    # Contact
    path('send_contact_email/', views.send_contact),
    path('send_email/', views.send_email),
    # Events
    path('my_events/', views.my_events),
    path('event_page/<str:event_id>', views.event_page),
    path('attendees/', views.attendees_page),
    path('eventcreation/<str:idd>/<str:title>/<str:description>/<str:start>/<str:end>/<str:duration>/', views.eventcreation)
]
