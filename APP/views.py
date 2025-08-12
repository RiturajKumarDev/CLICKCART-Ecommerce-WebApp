from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from APP.models import *
from Products.models import *
from Order.models import *
import random


def home(request):
    products = list(Product.objects.all())
    random.shuffle(products)
    productsFirstRow = products[:6]
    productsSecondRow = products[6:12]
    productsThirdRow = products[12:18]
    productsFourthRow = products[18:24]
    context = {
        "productsFirstRow": productsFirstRow,
        "productsSecondRow": productsSecondRow,
        "productsThirdRow": productsThirdRow,
        "productsFourthRow": productsFourthRow,
    }
    return render(request, "home.html", context)


def profile(request):
    if "email" not in request.session.keys():
        return render(request, "home.html")
    else:
        user = User.objects.filter(email=request.session["email"])
        address = Address.objects.filter(email=request.session["email"])
        orders = Order.objects.filter(email=request.session["email"])
        context = {
            "user": user.first(),
            "address": address,
            "orders": orders,
        }
        return render(request, "profile.html", context)


def deleteAddress(request):
    if "email" not in request.session.keys():
        return render(request, "home.html")
    else:
        address = Address.objects.get(AddId=request.GET["AddId"])
        address.delete()
        return profile(request)


def editAddress(request):
    if "email" not in request.session.keys():
        return render(request, "home.html")
    else:
        if request.method == "POST":
            address = Address()
            address.email = User.objects.get(email=request.session["email"])
            address.fullName = request.POST["fullName"]
            address.mobile = request.POST["phone"]
            address.alternateMobile = request.POST["alternateMobile"]
            address.pincode = request.POST["pincode"]
            address.fullAddress = request.POST["fullAddress"]
            address.landmark = request.POST["landmark"]
            address.cityDistric = request.POST["city"]
            address.state = request.POST["state"]
            address.country = request.POST["country"]
            address.save()
            return profile(request)
        else:
            try:
                address = Address.objects.get(AddId=request.GET["AddId"])
                return render(request, "editAddress.html", {"address": address})
            except:
                pass
        return render(request, "editAddress.html")


def registration(request):
    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.filter(email=email)
        if len(user):
            userStatus = "Email all ready registred!"
            return render(request, "login.html", {"userStatus": userStatus})
        else:
            user = User()
            user.fullName = request.POST["fullName"]
            user.email = request.POST["email"]
            user.password = request.POST["password"]
            user.mobile = request.POST["mobile"]
            user.save()
            userStatus = "Registration successfull."
        return render(request, "login.html", {"userStatus": userStatus})
    else:
        try:
            user = User.objects.get(email=request.GET["email"])
            return render(request, "login.html", {"user": user})
        except:
            pass
    if "email" not in request.session.keys():
        return render(request, "login.html")
    else:
        return home(request)


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.filter(email=email, password=password)
        if len(user):
            request.session["email"] = user.first().email
            request.session["fullName"] = user.first().fullName
            return home(request)
        return render(request, "login.html")
    if "email" not in request.session.keys():
        return render(request, "login.html")
    else:
        return home(request)


def logout(request):
    if "email" in request.session.keys():
        del request.session["email"]
        del request.session["fullName"]
    return render(request, "login.html")
