from django.db import models


class Event(models.Model): 
	"""
	title - The title of the event
	"""
	title = models.CharField(max_length=250)

