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
    path('redirect/', views.password_change),
    # availability
    path('my_availability/', views.my_availability),
    path('my_availability/google_calendar/', views.import_google_calendar_data),
    path('update_timezone/', views.update_timezone),
    # Users
    path('create_user/', views.createUser),
    path('login_page/', TemplateView.as_view(template_name="core/login_page.html")),
    path('login_user/', views.login_user),
    path('accounts/logout_user/', views.logout_user),
    path('signup_page/', TemplateView.as_view(template_name ="core/signup.html")),
    path('my_account/', views.my_account),
    path('password_change/', views.password_change),
    path('privacy_policy/', views.privacy_policy),
    # Contact
    path('send_contact_email/', views.send_contact),
    path('send_email/', views.send_email),
    # Events
    path('my_events/', views.my_events),
    path('event_page/<str:event_id>', views.event_page),
    path('attendees/', views.attendees_page),
    path('create_event_form/', views.get_create_event_form),
    path('failed_login/', views.failed_login)
    path('failed_login/', views.failed_login),
    path('event_page/change_event_title/', views.change_event_title),
    path('event_page/change_event_description/', views.change_event_description),
]
