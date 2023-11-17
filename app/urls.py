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
    path('dashboard/',views.homeAdmin,name='dashboard'),
    path('dashboard/products/',views.productsTable,name="productsTable"),
    path('dashboard/products/addProduct',views.addProduct,name='addProduct'),
    path('dashboard/products/updateProduct/<int:id>',views.updateProduct,name='updateProduct'),
    path('dashboard/products/deleteProduct/<int:id>',views.deleteProduct,name='deleteProduct'),
    path('dashboard/users/',views.userTable,name='userTable'),
    path('dashboard/users/addUser',views.addUser,name='addUser'),
    path('dashboard/users/updateUser/<int:id>',views.updateUser,name='updateUser'),
    path('dashboard/users/deleteUser/<int:id>',views.deleteUser,name='deleteUser'),
]