from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import LoginForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = "registration/login.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            form.add_error(None, "Wrong username or password")
            return self.form_invalid(form)
        login(self.request, user)
        return redirect("order-list")


class LogoutView(FormView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("user-login")
