from django.urls import path
from Order.views import *

app_name = "Order"

urlpatterns = [
    path("placedOrder", placedOrder, name="placedOrder"),
    path("success", success, name="success"),
    path("trackOrder", trackOrder, name="trackOrder"),
]
