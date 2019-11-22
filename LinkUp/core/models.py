from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    title - The title of the event
    """
    event_id = models.CharField(max_length=32, primary_key=True, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_owner', null=True)
    admins = models.ManyToManyField(User, related_name='event_admins')
    members = models.ManyToManyField(User, related_name='event_members')
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250, null=True)
    duration = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    potential_start_date = models.DateTimeField()
    potential_end_date = models.DateTimeField()
    final_start_date = models.DateTimeField(blank=True, null=True)
    final_end_date = models.DateTimeField(blank=True, null=True)


class Schedule(models.Model):
    availability = models.CharField(max_length=50000)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class EventSchedule(models.Model):
    availability = models.CharField(max_length=50000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')


class UserTimezone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone_str = models.CharField(max_length=50)
