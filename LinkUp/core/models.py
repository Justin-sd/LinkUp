from django.db import models


class Availability(models.Model):
	availability = models.CharField(max_length=1500)


class LinkUpUser(models.Model):
	email = models.EmailField(primary_key=True)
	predefinedSchedule = models.ForeignKey(Availability, on_delete=models.CASCADE, blank=True, null=True)
	user_name = models.CharField(max_length=30)
	password = models.CharField(max_length=50)


class Schedule(Availability):
	user = models.ForeignKey(LinkUpUser, on_delete=models.CASCADE)


class Event(models.Model): 
	"""
	title - The title of the event
	"""
	event_id = models.CharField(max_length=32, primary_key=True)
	owner = models.ForeignKey(LinkUpUser, on_delete=models.CASCADE, related_name='event_owner')
	admins = models.ManyToManyField(LinkUpUser, related_name='event_admins')
	members = models.ManyToManyField(LinkUpUser, related_name='event_members')
	title = models.CharField(max_length=250)
	description = models.CharField(max_length=250, null=True)
	duration = models.DecimalField(decimal_places=2, max_digits=12, null=True)
	potentialStartDate = models.DateTimeField()
	potentialEndDate = models.DateTimeField()
	finalStartDate = models.DateTimeField(blank=True, null=True)
	finalEndDate = models.DateTimeField(blank=True, null=True)
