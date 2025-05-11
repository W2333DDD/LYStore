from django.urls import path
from . import views
app_name = 'apppage'

urlpatterns = [
    path('', views.firstpage_show, name='firstpage'),


]