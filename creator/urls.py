from django.urls import path
from . import views

urlpatterns = [
    path('', views.widget, name='widget'),
    path('product-details/', views.product_details, name='product_details'),
]
