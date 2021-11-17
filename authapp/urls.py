from django.urls import path
from .views import *
urlpatterns = [
    path('',signupview, name='signup'),
    path('login/',loginview, name='login' ),
    path('loginsuccess/',loginsuccess, name='success' ),
    path('logout/', logoutview, name='logout'),
    path('password_reset/', password_reset_view, name='password_reset'),
]