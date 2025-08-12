from django.urls import path
from APP.views import *

app_name = "APP"

urlpatterns = [
    path("", home, name="home"),
    path("registration", registration, name="registration"),
    path("login", login, name="login"),
    path("profile", profile, name="profile"),
    path("editAddress", editAddress, name="editAddress"),
    path("deleteAddress", deleteAddress, name="deleteAddress"),
    path("logout", logout, name="logout"),
]
