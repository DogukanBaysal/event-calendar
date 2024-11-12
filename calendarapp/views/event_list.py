from django.views.generic import ListView

from calendarapp.models import Event

from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit


@method_decorator(ratelimit(key='ip', rate='20/m', method='GET'), name='get')
class AllEventsListView(ListView):
    """ All event list views """

    template_name = "calendarapp/events_list.html"
    model = Event
    
    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)

@method_decorator(ratelimit(key='ip', rate='20/m', method='GET'), name='get')
class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)

@method_decorator(ratelimit(key='ip', rate='20/m', method='GET'), name='get')
class UpcomingEventsListView(ListView):
    """ Upcoming events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_upcoming_events(user=self.request.user)
    
@method_decorator(ratelimit(key='ip', rate='20/m', method='GET'), name='get')
class CompletedEventsListView(ListView):
    """ Completed events list view """

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_completed_events(user=self.request.user)
    


