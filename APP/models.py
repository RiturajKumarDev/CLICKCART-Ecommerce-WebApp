from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=50, primary_key=True)
    fullName = models.CharField(null=False, max_length=30)
    password = models.CharField(null=False, max_length=20)
    mobile = models.IntegerField(default=0)

    def __str__(self):
        return self.email


class Address(models.Model):
    AddId = models.BigAutoField(primary_key=True, auto_created=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    fullName = models.CharField(null=False, max_length=30)
    mobile = models.IntegerField(default=0)
    alternateMobile = models.IntegerField(default=0)
    pincode = models.IntegerField(default=0)
    fullAddress = models.TextField(null=False, max_length=100)
    landmark = models.TextField(null=False, max_length=50)
    cityDistric = models.TextField(null=False, max_length=20)
    state = models.TextField(null=False, max_length=20)
    country = models.TextField(null=True, max_length=20)

    def __str__(self):
        return str(self.email.email)
