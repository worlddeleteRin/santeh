
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('contacts/', views.contacts, name = 'contacts'),
    path('delivery/', views.delivery, name = 'delivery'),
    path('payment/', views.payment, name = 'payment'),
    path('<int:cat_id>', views.category, name = 'category'),
    path('<int:cat_id>/<int:dest_id>', views.destination, name = 'destination'),
    path('product/<int:product_id>', views.product, name = 'product'),
    path('products/on_sale', views.on_sale, name = 'on_sale'),
    path('filter_products_ajax', views.filter_products_ajax, name = 'filter_products_ajax'),
    path('load_products_ajax', views.load_products_ajax, name = 'load_products_ajax'),
    path('search_form', views.search_form, name = 'search_form'),
    path('search/<search_query>', views.search, name = 'search')
]
