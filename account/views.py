from django.contrib.auth import get_user_model, views, authenticate, login
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import RegisterForm

User = get_user_model()


class PasswordChangeView(views.PasswordChangeView):
    success_url = reverse_lazy("index")


class PasswordResetView(views.PasswordResetView):
    success_url = reverse_lazy("account:password_reset_done")


class PasswordResetCompletionView(views.PasswordResetCompleteView):
    pass


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy("account:password_reset_complete")


class PasswordResetDoneView(views.PasswordResetDoneView):
    pass


class LoginView(views.LoginView):
    template_name = "account/login.html"


class LogoutView(views.LogoutView):
    pass


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = "/"
    template_name = "account/register.html"

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("index")
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)
