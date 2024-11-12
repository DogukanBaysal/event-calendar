from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from calendarapp.models import Event


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET'))
    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.get_latest_events(user=request.user)
        completed_events = Event.objects.get_completed_events(user=request.user)
        upcoming_events = Event.objects.get_upcoming_events(user=request.user)
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
            "completed_events": completed_events.count(),
            "upcoming_events": upcoming_events
        }
        return render(request, self.template_name, context)
