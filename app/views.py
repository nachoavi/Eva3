from django.shortcuts import render,redirect,HttpResponse
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
    return render(request,'adShop/productsCrud/tableProds.html')

def addProduct(request):
    return render(request,'adShop/productsCrud/addProds.html')

def userTable(request):
    return render(request,'adShop/userCrud/userTable.html')

def addUser(request):
    return render(request,'adShop/userCrud/addUser.html')

