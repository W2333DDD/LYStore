from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('store_enroll',views.register_shop,name='store_enroll'),
    path('my_store',views.my_shop,name='my_store'),
    path('detail/<int:pk>/', views.store_detail, name='store_detail'),
]