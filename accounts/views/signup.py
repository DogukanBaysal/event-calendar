from django.views.generic import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from accounts.forms import SignUpForm


class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    @method_decorator(ratelimit(key='ip', rate='15/m', method='POST'))
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        print(forms)
        if forms.is_valid():
            forms.save()
            return redirect("accounts:signin")
        context = {"form": forms}
        return render(request, self.template_name, context)
