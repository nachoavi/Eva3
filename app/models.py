from django.db import models

# Create your models here.

class Roles(models.Model):
    role = models.CharField(max_length=50)
    
class Users(models.Model):
    name = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    email = models.EmailField(max_length=255, null=False)
    address = models.TextField(blank=True, null=True)
    username = models.CharField(max_length=50,null=False)
    password = models.CharField(max_length=50,null=False)
    cart = models.OneToOneField('ShoppingCart', on_delete=models.CASCADE,null=True)
    credits = models.IntegerField(null=False,default=0)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT)
    

class Products(models.Model):
    name = models.CharField(max_length=255,null=False)
    description = models.TextField(null=False)
    price = models.PositiveIntegerField(null=False)
    stock = models.PositiveIntegerField(null=False)
    
class ShoppingCart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    productsInCart = models.ManyToManyField(Products,through='ItemCart')
    createdAt = models.DateTimeField(auto_now_add=True)
    
class ItemCart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1,null=False)
    
class Order(models.Model):
    cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    address = models.TextField(null=False)
    total = models.PositiveIntegerField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    isProcessed = models.BooleanField(default=False)
    

