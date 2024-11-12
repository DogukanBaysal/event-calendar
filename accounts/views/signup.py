from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from honeypot.decorators import check_honeypot

from accounts.forms import SignUpForm

@method_decorator(check_honeypot(field_name="Email"), name='post')
@method_decorator(check_honeypot(field_name="Password1"), name='post')
@method_decorator(check_honeypot(field_name="Password2"), name='post')
class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET'))
    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST'))
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("accounts:signin")
        context = {"form": forms}
        return render(request, self.template_name, context)
