from django.shortcuts import render
from django.conf import settings
import razorpay
from django.utils.timezone import now
from datetime import timedelta
from APP.models import *

