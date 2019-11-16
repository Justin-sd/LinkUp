from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
	"""
	title - The title of the event
	"""
	event_id = models.CharField(max_length=32, primary_key=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner')
	admins = models.ManyToManyField(User, related_name='event_admins')
	members = models.ManyToManyField(User, related_name='event_members')
	title = models.CharField(max_length=250)
	description = models.CharField(max_length=250, null=True)
	duration = models.DecimalField(decimal_places=2, max_digits=12, null=True)
	potentialStartDate = models.DateTimeField()
	potentialEndDate = models.DateTimeField()
	finalStartDate = models.DateTimeField(blank=True, null=True)
	finalEndDate = models.DateTimeField(blank=True, null=True)


class Schedule(models.Model):
	availability = models.CharField(max_length=50000)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class EventSchedule(Schedule):
	event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
