from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from user.forms import RegisterForm


class RegisterView(CreateView):
    template_name = 'user/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('user:login')


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = AuthenticationForm
    # success_url = reverse_lazy('profile')


def logout_func(request):
    logout(request)
    return redirect('questionnaire:list_questions')
