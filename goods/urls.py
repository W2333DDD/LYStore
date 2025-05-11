from django.urls import path
from . import admin
from . import views

app_name = 'goods'

urlpatterns = [
#    path('admin/', admin.site.urls),
    path('create_good',views.create_product,name='create_good'),
    path('<int:pk>/', views.good_detail, name='good_detail'),
    path('product/<int:pk>/create-tripo/', views.create_tripo_model, name='create_tripo_model'),
    path('product/<int:pk>/check-tripo/', views.check_tripo_model_status, name='check_tripo_model_status'),
    path('product/<int:pk>/product_show/', views.product_show, name='product_show'),
    path('product_search/', views.search_view, name='search_view'),
    path('product/<int:product_id>/add_comment/', views.add_comment, name='add_comment'),


]