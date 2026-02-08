from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Products(models.Model):
    pname = models.CharField(max_length=25)
    pdesc = models.CharField(max_length=100)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=30)
    trending = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    pimage = models.ImageField(upload_to='uploads',default='default.jpg')

class CartModel(models.Model):
    pname = models.CharField(max_length=25)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=30)
    quantity = models.IntegerField()
    totalprice = models.IntegerField()
    host = models.ForeignKey(User,on_delete=models.CASCADE)
