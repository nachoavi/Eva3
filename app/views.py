from django.shortcuts import render,redirect,HttpResponse
from .models import *

# Create your views here.

def home(request):
    return render(request,'shop/index.html')

def signin(request):
    return render(request,'signin.html')

def signup(request):
    return render(request,'signup.html')

def catalog(request):
    return render(request,'shop/catalog.html')

def shopCart(request):
    return render(request,'shop/sCart.html')


#ADMIN ONLY

def homeAdmin(request):
    return render(request,'adShop/index.html')

def productsTable(request):
    return render(request,'adShop/productsCrud/tableProds.html')

def addProduct(request):
    return render(request,'adShop/productsCrud/addProds.html')

