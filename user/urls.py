from django.urls import path
from user.apps import UserConfig
from user.views import RegisterView, CustomLoginView, logout_func

app_name = UserConfig.name
urlpatterns = [
    path('', RegisterView.as_view(template_name='user/registration.html'), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_func, name='logout')
]
