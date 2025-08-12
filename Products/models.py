from django.db import models
from django.db.models import PROTECT
from APP.models import *


class Product(models.Model):
    productId = models.BigAutoField(primary_key=True, auto_created=True)
    sellerEmail = models.ForeignKey(User, on_delete=models.CASCADE)
    productType = models.CharField(null=False, max_length=30)
    productName = models.CharField(null=False, max_length=30)
    productPrice = models.FloatField(default=0)
    productTitle = models.CharField(null=False, max_length=100)
    productBrand = models.CharField(null=False, max_length=30)
    productWork = models.CharField(null=False, max_length=30)
    fullDetails = models.CharField(null=False, max_length=500)
    images = models.JSONField(default=dict)
    videos = models.JSONField(default=dict)
    keysFeatures = models.JSONField(default=dict)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.productName)


class MyCart(models.Model):
    cartId = models.BigAutoField(primary_key=True, auto_created=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    noOfProduct = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.email.email)
