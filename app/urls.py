from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='index'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('shop/catalog',views.catalog,name='catalog'),
    path('shop/shopCart',views.shopCart,name='shopCart'),
    path('indexAdmin/',views.homeAdmin,name='homeAdmin'),
    path('products/',views.productsTable,name="productsTable"),
    path('products/addProduct',views.addProduct,name='addProduct'),
    path('products/updateProduct/<int:id>',views.updateProduct,name='updateProduct'),
    path('products/deleteProduct/<int:id>',views.deleteProduct,name='deleteProduct'),
    path('users/',views.userTable,name='userTable'),
    path('users/addUser',views.addUser,name='addUser'),
    path('users/updateUser/<int:id>',views.updateUser,name='updateUser'),
    path('users/deleteUser/<int:id>',views.deleteUser,name='deleteUser'),
]