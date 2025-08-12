from django.db import models
from APP.models import *
from Order.models import *


class PaymentDetails(models.Model):
    paymentDetailsId = models.BigIntegerField(primary_key=True, auto_created=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    date = models.DateField(null=True)

    def __str__(self):
        return str(self.email.email)
