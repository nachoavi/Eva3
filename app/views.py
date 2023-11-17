from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import bcrypt

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
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_encrypt = generate_encrypt_password(password)


        new_user = Users(name=name, lastname=lastname, email=email, username=username, password=password_encrypt)

        new_user.save()

        return redirect("signup")
    else:
        return render(request,'signup.html')
    
def logout(request):
    del request.session['isAuthenticated']
    return redirect("/")

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
    
        

