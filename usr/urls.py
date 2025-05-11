from django.urls import path
from . import views

app_name = 'usr'

urlpatterns = [
    path('log_in',views.login_view, name='login'),
    path('enroll_in',views.register_view, name='register'),
    path('log_out',views.logout_view, name='logout'),
    path('usr_home',views.usr_home, name='usrhome'),
]