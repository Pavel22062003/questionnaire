from django.contrib.auth.forms import UserCreationForm

from user.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
