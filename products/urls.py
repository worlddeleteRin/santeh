
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:cat_id>', views.category, name = 'category'),
    path('<int:cat_id>/<int:dest_id>', views.destination, name = 'destination'),
    path('product/<int:product_id>', views.product, name = 'product'),
    path('products/on_sale', views.on_sale, name = 'on_sale'),
    path('filter_products_ajax', views.filter_products_ajax, name = 'filter_products_ajax'),
    path('load_products_ajax', views.load_products_ajax, name = 'load_products_ajax'),
]
