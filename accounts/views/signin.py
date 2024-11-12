from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from honeypot.decorators import check_honeypot


from accounts.forms import SignInForm


@method_decorator(check_honeypot(field_name="Email"), name='post')
@method_decorator(check_honeypot(field_name="Password"), name='post')
class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    form_class = SignInForm

    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET'))
    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    
    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST'))
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(username=email, email=email, password=password, request=request)
            if user:
                login(request, user)
                return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)
