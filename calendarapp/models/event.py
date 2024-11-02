from base64 import b64decode
from datetime import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from cryptography.fernet import Fernet
from calendarapp.models import EventAbstract
from accounts.models import User
import bleach


dbKey = (settings.DATABASE_SECURITY_KEY).encode()
fernet = Fernet(dbKey)


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        for event in events:
            print(event.description)
            event.title = bleach.clean(fernet.decrypt(event.title.encode()).decode())
            event.description = bleach.clean(fernet.decrypt(event.description.encode()).decode())
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
            running_event.title = bleach.clean(fernet.decrypt(running_event.title.encode()).decode())
            running_event.description = bleach.clean(fernet.decrypt(running_event.description.encode()).decode())
        return running_events
    
    def get_completed_events(self, user):
        completed_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__lt=datetime.now().date(),
        )
        for completed_event in completed_events:
            completed_event.title = bleach.clean(fernet.decrypt(completed_event.title.encode()).decode())
            completed_event.description = bleach.clean(fernet.decrypt(completed_event.description.encode()).decode())
        return completed_events
    
    def get_upcoming_events(self, user):
        upcoming_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            start_time__gt=datetime.now().date(),
        )
        for upcoming_event in upcoming_events:
            upcoming_event.title = bleach.clean(fernet.decrypt(upcoming_event.title.encode()).decode())
            upcoming_event.description = bleach.clean(fernet.decrypt(upcoming_event.description.encode()).decode())
        return upcoming_events
    

    def get_latest_events(self, user):
        running_events = Event.objects.filter(user=user).order_by("-id")[:10]
        for running_event in running_events:
            running_event.title = bleach.clean(fernet.decrypt(running_event.title.encode()).decode())
            running_event.description = bleach.clean(fernet.decrypt(running_event.description.encode()).decode())
        return running_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=200)
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
