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
    path('event_page/<str:event_id>', views.event_page),
    path('my_events/<str:user_name>', views.my_events),
    path('attendees/', views.attendees_page),
    path('login_page/', TemplateView.as_view(template_name="core/login_page.html")),
    path('/accounts/logout', TemplateView.as_view()),
    path('my_events/', views.my_events),
    path('attendees/', views.attendees_page),
    path('login_page/', TemplateView.as_view(template_name="core/login_page.html")),
    path('my_availability/', views.my_availability),
    path('about', views.about),
    path('contact', views.contact),
    path('reportanissue', views.report_an_issue),
    path('donate', views.donate),
    path('support', views.support),
]

