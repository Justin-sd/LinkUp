from django.db import models

# Create your models here.

class Event(models.Model): 
	'''
	title - The title of the event
	'''

	title = models.CharField(max_length = 250)

	
