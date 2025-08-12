from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from django.db.models import Q
from APP.models import *
from APP.views import *
from Products.models import *


def sellProduct(request):
    if "email" not in request.session.keys():
        return registration(request)
    elif request.method == "POST":
        product = Product()
        product.sellerEmail = User.objects.get(email=request.session["email"])
        product.productType = request.POST["productType"]
        product.productName = request.POST["productName"]
        product.productPrice = request.POST["productPrice"]
        product.productTitle = request.POST["productTitle"]
        product.productBrand = request.POST["productBrand"]
        product.productWork = request.POST["productWork"]
        product.fullDetails = request.POST["fullDetails"]
        dImg = dict()
        dVid = dict()
        listKeys = list()
        listFeatures = list()
        for key in request.FILES:
            file = request.FILES[key]
            if key.startswith("img"):
                path = default_storage.save(f"product_images/{file.name}", file)
                dImg[key] = default_storage.url(path)
            elif key.startswith("vid"):
                try:
                    path = default_storage.save(f"product_videos/{file.name}", file)
                    dVid[key] = default_storage.url(path)
                except:
                    pass
        for key in request.POST:
            if key.startswith("key"):
                listKeys.append(request.POST[key])
            elif key.startswith("feature"):
                listFeatures.append(request.POST[key])
        kf = dict()
        i = 0
        for e in listKeys:
            kf[e] = listFeatures[i]
            i += 1
        product.images = dImg
        product.videos = dVid
        product.keysFeatures = kf
        product.save()
    return render(request, "sellProduct.html")


def searchProduct(request):
    if request.method == "POST":
        search = str(request.POST["search"]).lower()
        products = []
        for product in Product.objects.all():
            if search in str(vars(product)).lower():
                products.append(product)
        if len(products) == 0:
            return home(request)
        return render(request, "searchProduct.html", {"products": products})
    else:
        search = str(request.GET["search"]).lower()
        products = []
        for product in Product.objects.all():
            if search in str(vars(product)).lower():
                products.append(product)
        if len(products) == 0:
            return home(request)
        return render(request, "searchProduct.html", {"products": products})


def productPage(request):
    try:
        mainProduct = Product.objects.get(productId=request.GET["productId"])
        products = []
        productType = str(mainProduct.productType).lower()
        for product in Product.objects.all():
            if productType in str(vars(product)).lower():
                products.append(product)
        context = {
            "product": mainProduct,
            "products": products,
        }
        return render(request, "productPage.html", context)
    except:
        return home(request)


def cartPage(request):
    if "email" not in request.session.keys():
        return home(request)
    elif request.method == "POST":
        productid = request.POST["productId"]
        product = Product.objects.get(productId=productid)
        mycart = MyCart.objects.filter(email=request.session["email"])
        find = True
        if len(mycart):
            for cart in mycart:
                if cart.product.productId == product.productId:
                    mycart = MyCart()
                    mycart.cartId = cart.cartId
                    mycart.email = cart.email
                    mycart.product = cart.product
                    mycart.noOfProduct = cart.noOfProduct + 1
                    mycart.price = mycart.product.productPrice * mycart.noOfProduct
                    mycart.save()
                    find = False
                    break
            if find:
                mycart = MyCart()
                mycart.email = User.objects.get(email=request.session["email"])
                mycart.product = Product.objects.get(productId=productid)
                mycart.noOfProduct = 1
                mycart.price = mycart.product.productPrice
                mycart.save()
        else:
            mycart = MyCart()
            mycart.email = User.objects.get(email=request.session["email"])
            mycart.product = Product.objects.get(productId=productid)
            mycart.noOfProduct = 1
            mycart.price = mycart.product.productPrice
            mycart.save()

    mycart = MyCart.objects.filter(email=request.session["email"])
    address = Address.objects.filter(email=request.session["email"])
    context = {
        "address": address,
        "add": address.first(),
        "mycart": mycart,
    }
    return render(request, "cartPage.html", context)


def deleteCart(request):
    if "email" not in request.session.keys():
        return home(request)
    cartId = request.GET["cartId"]
    cart = MyCart.objects.get(cartId=cartId)
    cart.delete()
    mycart = MyCart.objects.filter(email=request.session["email"])
    return render(request, "cartPage.html", {"mycart": mycart})


def addCart(request):
    if "email" not in request.session.keys():
        return home(request)
    cartId = request.GET["cartId"]
    cart = MyCart.objects.get(cartId=cartId)

    mycart = MyCart()
    mycart.cartId = cart.cartId
    mycart.email = cart.email
    mycart.product = cart.product
    mycart.noOfProduct = cart.noOfProduct + 1
    mycart.price = mycart.product.productPrice * mycart.noOfProduct
    mycart.save()

    mycart = MyCart.objects.filter(email=request.session["email"])
    return render(request, "cartPage.html", {"mycart": mycart})


def discartCart(request):
    if "email" not in request.session.keys():
        return home(request)
    cartId = request.GET["cartId"]
    cart = MyCart.objects.get(cartId=cartId)
    if cart.noOfProduct == 1:
        cart.delete()
    else:
        mycart = MyCart()
        mycart.cartId = cart.cartId
        mycart.email = cart.email
        mycart.product = cart.product
        mycart.noOfProduct = cart.noOfProduct - 1
        mycart.price = mycart.product.productPrice * mycart.noOfProduct
        mycart.save()

    mycart = MyCart.objects.filter(email=request.session["email"])
    return render(request, "cartPage.html", {"mycart": mycart})
