from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
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
    products = Products.objects.all()
    if request.method == 'GET':
        return render(request,'adShop/productsCrud/tableProds.html',{'products':products})

def addProduct(request):
    if request.method == 'GET':
        categorys = ProductCategory.objects.all()
        return render(request,'adShop/productsCrud/addProds.html',{'categorys':categorys})
    else:
        categorySelected = ProductCategory.objects.get(id=request.POST.get('category'))
        newProd = Products.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            category=categorySelected,
            stock=request.POST['stock'],
            urlImage=request.POST['urlImage']
        )
        newProd.save()
        return redirect('productsTable')
    
def updateProduct(request,id):
    productToUpdate = get_object_or_404(Products,id=id)
    if request.method == 'GET':
        categorys = ProductCategory.objects.all()
        return render(request, 'adShop/productsCrud/updateProds.html',{'productToUpdate':productToUpdate,'categorys':categorys})
    else:
        categorySelected = ProductCategory.objects.get(id=request.POST.get('category'))
        productToUpdate.name = request.POST.get('name')
        productToUpdate.description = request.POST.get('description')
        productToUpdate.price = request.POST.get('price')
        productToUpdate.category = categorySelected
        productToUpdate.stock = request.POST.get('stock')
        productToUpdate.urlImage= request.POST.get('urlImage')
        productToUpdate.save()
        return redirect('productsTable')
    
def deleteProduct(request,id):
    productToDelete = Products.objects.get(id=id)
    productToDelete.delete()
    return redirect('productsTable')
    
    
    
def userTable(request):
    users = Users.objects.all()
    if request.method == 'GET':
        return render(request,'adShop/userCrud/userTable.html',{'users':users})
   

def addUser(request):
    if request.method == 'GET':
        roles = Roles.objects.all()
        return render(request,'adShop/userCrud/addUser.html',{'roles':roles})
    else:
        roleSelected = Roles.objects.get(id=request.POST.get('role'))
        newUser = Users.objects.create(
            name=request.POST['name'],
            lastname=request.POST['lastname'],
            email=request.POST['email'],
            address=request.POST['address'],
            username=request.POST['username'],
            password=request.POST['password'],
            role=roleSelected
        )
        newUser.save()
        return redirect('userTable')
    
def updateUser(request,id):
    userToUpdate = get_object_or_404(Users,id=id)
    if request.method == 'GET':
        roles = Roles.objects.all()
        return render(request, 'adShop/userCrud/updateUser.html',{'userToUpdate':userToUpdate,'roles':roles})
    else:
        roleSelected = Roles.objects.get(id=request.POST.get('role'))
        userToUpdate.name = request.POST.get('name')
        userToUpdate.lastname = request.POST.get('lastname')
        userToUpdate.email = request.POST.get('email')
        userToUpdate.address = request.POST.get('address')
        userToUpdate.username = request.POST.get('username')
        userToUpdate.password = request.POST.get('password')
        userToUpdate.role = roleSelected
        userToUpdate.save()
        return redirect('userTable')
        
    
def deleteUser(request,id):
    userToDelete = Users.objects.get(id=id)
    userToDelete.delete()
    return redirect('userTable')
    
        

