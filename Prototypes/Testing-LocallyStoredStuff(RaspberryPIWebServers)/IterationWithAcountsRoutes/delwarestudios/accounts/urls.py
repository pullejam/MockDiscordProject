
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signupPage, name="signup"),
    path('login/', views.loginPage, name="login"),
]