from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='index'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('shop/catalog',views.catalog,name='catalog'),
    path('shop/shopCart',views.shopCart,name='shopCart'),
    path('products/',views.productsTable,name="productsTable"),
    
    
]