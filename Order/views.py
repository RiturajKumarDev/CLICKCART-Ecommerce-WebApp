from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from APP.models import *
from Products.models import *
from Order.models import *
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
import razorpay
import random


rpay = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def placedOrder(request):
    if "email" not in request.session.keys():
        return render(request, "home.html")
    elif request.method == "POST":
        user = User.objects.get(email=request.session["email"])
        try:
            cartId = request.POST["cartId"]
            myCarts = MyCart.objects.filter(cartId=cartId)
        except:
            myCarts = MyCart.objects.filter(email=request.session["email"])
        order = Order()
        totalPrice = 0
        for cart in myCarts:
            totalPrice += cart.price
        if totalPrice == 0:
            return redirect("/cartPage")
        order.myCarts = [
            {
                "productId": cart.product.productId,
                "quantity": cart.noOfProduct,
                "productTitle": cart.product.productTitle,
                "productName": cart.product.productName,
                "price": cart.price,
                "productBrand": cart.product.productBrand,
                "image": cart.product.images["img1"] if cart.product.images else "",
            }
            for cart in myCarts
        ]
        for cart in myCarts:
            cart.delete()
        order.address = Address.objects.get(AddId=request.POST["addressId"])
        order.email = User.objects.get(email=request.session["email"])
        order.totalPrice = totalPrice
        order.paymentStatus = False
        order.save()

        orderId = order.orderId

        orderPath = OrderPath()
        orderPath.order = Order.objects.get(orderId=orderId)
        orderPath.confirmDate = now()
        orderPath.shippedDate = now() + timedelta(days=1)
        orderPath.outOfDeliveryDate = now() + timedelta(days=6)
        orderPath.deliveredDate = now() + timedelta(days=7)
        orderPath.save()

        order = Order.objects.get(orderId=orderId)

        updateOrder = Order()
        updateOrder.orderId = orderId
        updateOrder.myCarts = order.myCarts
        updateOrder.address = Address.objects.get(AddId=request.POST["addressId"])
        updateOrder.email = User.objects.get(email=request.session["email"])
        updateOrder.totalPrice = totalPrice
        updateOrder.paymentStatus = False
        updateOrder.trackPath = OrderPath.objects.get(orderPathId=orderPath.orderPathId)
        updateOrder.save()

        order = rpay.order.create(
            {
                "amount": totalPrice * 100,
                "currency": "INR",
                "payment_capture": "1",
            }
        )
        context = {
            "amount": totalPrice * 100,
            "order": updateOrder,
            "orderId": orderId,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "showAmount": totalPrice,
        }
        if request.POST["payment"] == "YES":
            return render(request, "paymentPage.html", context)
        return render(request, "success.html", context)


def success(request):
    if "email" not in request.session.keys():
        return render(request, "home.html")
    elif request.method == "POST":
        para = {
            key: request.POST.get(key)
            for key in [
                "amount",
                "razorpay_payment_id",
                "razorpay_order_id",
                "razorpay_signature",
            ]
        }
        if None in para.values():
            return render(request, "paymentPage.html")
        try:
            rpay.utility.verify_payment_signature(para)
            # update data in database
            order = Order.objects.filter(email=request.session["email"]).last()

            updateOrder = Order()
            updateOrder.orderId = order.orderId
            updateOrder.myCarts = order.myCarts
            updateOrder.address = order.address
            updateOrder.email = User.objects.get(email=request.session["email"])
            updateOrder.totalPrice = order.totalPrice
            updateOrder.paymentStatus = True
            updateOrder.trackPath = order.trackPath
            updateOrder.save()
            context = {
                "order": Order.objects.filter(email=request.session["email"]).last()
            }
            return render(request, "success.html", context)

        except:
            return render(request, "paymentPage.html")
    return render(request, "paymentPage.html")


def trackOrder(request):
    if "email" not in request.session.keys():
        return render(request, "home.html")
    else:
        trackPathId = request.GET["trackPathId"]
        orderPath = OrderPath.objects.get(orderPathId=trackPathId)
        return render(request, "trackOrder.html", {"orderPath": orderPath})
