
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authapp.urls')),
path('password_reset/done/',
         views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
