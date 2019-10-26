from django.db import models


class Event(models.Model): 
	"""
	title - The title of the event
	"""
	event_id = models.CharField(max_length=32, primary_key=True)
	title = models.CharField(max_length=250)
	description = models.CharField(max_length=250, null=True)

