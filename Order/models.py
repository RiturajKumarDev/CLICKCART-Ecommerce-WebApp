from django.db import models
from APP.models import *
from Products.models import *


class Order(models.Model):
    orderId = models.BigAutoField(primary_key=True, auto_created=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    totalPrice = models.FloatField(default=0)
    orderDate = models.DateField(auto_now=True)
    myCarts = models.JSONField(default=list)
    paymentStatus = models.BooleanField(default=False)
    trackPath = models.ForeignKey('OrderPath', null=True, on_delete=models.SET_NULL, related_name='tracked_orders')


    def __str__(self):
        return str(self.email.email)


class OrderPath(models.Model):
    orderPathId = models.BigAutoField(primary_key=True, auto_created=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    confirmDate = models.DateField(null=True)
    shippedDate = models.DateField(null=True)
    outOfDeliveryDate = models.DateField(null=True)
    deliveredDate = models.DateField(null=True)
    cancelledDate = models.DateField(null=True)
    returnDate = models.DateField(null=True)
    refundDate = models.DateField(null=True)

    def __str__(self):
        return str(self.order.email.email)
