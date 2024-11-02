from base64 import b64decode
from datetime import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
import rsa

from calendarapp.models import EventAbstract
from accounts.models import User

privateKey = rsa.PrivateKey(settings.PRIVATE_KEY_N, settings.PRIVATE_KEY_E, settings.PRIVATE_KEY_D, settings.PRIVATE_KEY_P, settings.PRIVATE_KEY_Q)

class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        for event in events:
            event.title = rsa.decrypt(b64decode(event.title), privateKey).decode('utf8')
            event.description = rsa.decrypt(b64decode(event.description), privateKey).decode('utf8')
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
            start_time__lte = datetime.now().date()
        ).order_by("start_time")
        
        for running_event in running_events:
            running_event.title = rsa.decrypt(b64decode(running_event.title), privateKey).decode('utf8')
            running_event.description = rsa.decrypt(b64decode(running_event.description), privateKey).decode('utf8')
        return running_events
    
    def get_completed_events(self, user):
        completed_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__lt=datetime.now().date(),
        )
        for completed_event in completed_events:
            completed_event.title = rsa.decrypt(b64decode(completed_event.title), privateKey).decode('utf8')
            completed_event.description = rsa.decrypt(b64decode(completed_event.description), privateKey).decode('utf8')
        return completed_events
    
    def get_upcoming_events(self, user):
        upcoming_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__gt=datetime.now().date(),
        )
        for upcoming_event in upcoming_events:
            upcoming_event.title = rsa.decrypt(b64decode(upcoming_event.title), privateKey).decode('utf8')
            upcoming_event.description = rsa.decrypt(b64decode(upcoming_event.description), privateKey).decode('utf8')
        return upcoming_events
    

    def get_latest_events(self, user):
        running_events = Event.objects.filter(user=user).order_by("-id")[:10]
        for running_event in running_events:
            running_event.title = rsa.decrypt(b64decode(running_event.title), privateKey).decode('utf8')
            running_event.description = rsa.decrypt(b64decode(running_event.description), privateKey).decode('utf8')
        return running_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
