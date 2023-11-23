from django.db import models

# Crea te your models here.

class Roles(models.Model):
    role = models.CharField(max_length=50)
    
class Users(models.Model):
    name = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    email = models.EmailField(max_length=255, null=False)
    address = models.CharField(max_length=255,blank=True, null=True)
    username = models.CharField(max_length=50,null=False)
    password = models.BinaryField(max_length=50,null=False)
    credits = models.IntegerField(null=False,default=0)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, default=1)

class ProductCategory(models.Model):
    category = models.CharField(max_length=100,null=False)

class Products(models.Model):
    name = models.CharField(max_length=255,null=False)
    description = models.TextField(null=False)
    price = models.PositiveIntegerField(null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    stock = models.PositiveIntegerField(null=False)
    urlImage = models.URLField(null=False)
        
    
class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT)
    address = models.CharField(max_length=255,null=False)
    products = models.ManyToManyField(Products)
    total = models.PositiveIntegerField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    isProcessed = models.BooleanField(default=False)
    

