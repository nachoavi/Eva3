from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum,F
from django.core.exceptions import ObjectDoesNotExist
from functools import wraps
import bcrypt
import json

# Create your views here. 

def generate_encrypt_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)

    return hash

def login_check_password(password_entry, password_db):
    encode_pass = password_entry.encode('utf-8')
    result = bcrypt.checkpw(encode_pass, password_db)
    return result

def home(request):
    print(request.session.get("role"))
    return render(request,'shop/index.html')

def signin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = Users.objects.get(username=username)
            login_check = login_check_password(password, user.password)
        
            if login_check:
                request.session["isAuthenticated"] = True
                request.session["id"] = user.id
                request.session["role"] = user.role_id
                return redirect("/")
            else:
                return render(request,'signin.html', {"error": "error"})

        
        except ObjectDoesNotExist:
            return render(request,'signin.html', {"error": "error"})
    else:
        return render(request,'signin.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_encrypt = generate_encrypt_password(password)

        new_user = Users(name=name, lastname=lastname, email=email, address=address, username=username, password=password_encrypt)

        new_user.save()

        return redirect("/signin")
    else:
        return render(request,'signup.html')
    
def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = request.session.get('id')
        if not user_id:
            return redirect('signin')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
    
    
def logout(request):
    del request.session['isAuthenticated']
    del request.session['id']
    del request.session['role']
    
    return redirect("/")

def catalog(request):
    products = Products.objects.all()
    if request.method == 'GET':
        return render(request,'shop/catalog.html',{'products':products})


def addToCart(request,id):
    productSelected = get_object_or_404(Products,id=id)
    
    if productSelected.stock <= 0:
        messages.error(request,'No existe stock de este producto')
        return redirect('catalog')
        
    
    if 'cart' not in request.session:
        request.session['cart'] = []    
    
    cart = request.session['cart']
    cart.append({
        'id':productSelected.id,
        'name': productSelected.name,
        'description': productSelected.description,
        'price': productSelected.price,
        'category': productSelected.category.category,
        'stock': productSelected.stock,
        'urlImage': productSelected.urlImage,
        'quantity': 1
    })
    
    request.session['cart'] = cart
    
    return redirect('catalog')

def shopCart(request):
    cart = request.session.get('cart',[])
    total = sum(item['price'] for item in cart)
    return render(request,'shop/sCart.html',{'cart':cart,'total':total})

def dellToCart(request,id):
    if 'cart' in request.session:
        cart = request.session['cart']
        
        for item in cart:
            if item['id'] == id:
                
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    cart.remove(item)
                
                request.session['cart'] = cart
                request.session.save()
                break
   
    return redirect('shopCart')

def emptyCart(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.save()
    return redirect('shopCart')

@custom_login_required
def confirmOrder(request):
    user =  request.session["id"]
    userInSession = Users.objects.get(id=user)
    cart = request.session.get('cart',[])
    
    if not cart:
        messages.error(request,'No hay nada que pagar aquí:)')
        return redirect('shopCart')
    
    total = sum(item['price'] for item in cart)
    productID = cart[0].get('id')
    productName = cart[0].get('name')
    
    products = Products.objects.filter(id=productID)
    
    
    newOrder = Order.objects.create(
        user=userInSession,
        address=userInSession.address,
        total=total
        )
    newOrder.products.set(products)
    
    
    for item in Products.objects.filter(name=productName):

            if item.stock == 0:
                messages.error(request,'No existe stock')
                return redirect('shopCart')
            else:
                for product in cart:
                    item.stock -= product['quantity']
                    item.save()

    newOrder.isProcessed = True    
    newOrder.save()
    
    del request.session['cart']

    last_order = Order.objects.filter(user=userInSession).last()

    
    return render(request, "shop/orderDetail.html", {"last_order": last_order,'products':products})

        
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
        password = request.POST.get("password")
        password_encrypt = generate_encrypt_password(password)
        newUser = Users.objects.create(
            name=request.POST['name'],
            lastname=request.POST['lastname'],
            email=request.POST['email'],
            address=request.POST['address'],
            username=request.POST['username'],
            password=password_encrypt,
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
        userToUpdate.password = generate_encrypt_password(request.POST.get('password'))
        userToUpdate.role = roleSelected
        userToUpdate.save()
        return redirect('userTable')
        
     
def deleteUser(request,id):
    userToDelete = Users.objects.get(id=id)
    userToDelete.delete()
    return redirect('userTable')
    
def viewSales(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        return render(request,'adShop/sales/viewSales.html',{'orders':orders})
        

