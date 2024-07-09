from django.urls import path
from . import views

urlpatterns = [
    path('', views.widget, name='widget'),
    path('landing-page-creator', views.landing_page_creator, name='landing_page_creator'),
    path('product-details/', views.product_details, name='product_details'),
    path('add_to_file/', views.add_to_file, name='add_to_file'),
    path('display_file_content/', views.display_file_content, name='display_file_content'),
    path('clear_file_content/', views.clear_file_content, name='clear_file_content')
]
