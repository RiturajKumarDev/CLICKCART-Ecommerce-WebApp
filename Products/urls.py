from django.urls import path
from Products.views import *

app_name = "Products"

urlpatterns = [
    path("sellProduct", sellProduct, name="sellProduct"),
    path("searchProduct", searchProduct, name="searchProduct"),
    path("productPage", productPage, name="productPage"),
    path("cartPage", cartPage, name="cartPage"),
    path("deleteCart", deleteCart, name="deleteCart"),
    path("addCart", addCart, name="addCart"),
    path("discartCart", discartCart, name="discartCart"),
]
