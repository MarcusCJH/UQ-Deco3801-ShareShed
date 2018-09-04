from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def louis(request, random_number):
    return HttpResponse("Hello, world. " + str(random_number))

def risyad(request, random_number):
    return HttpResponse("Hello, world. " + str(random_number))

def paymenttest(request):
    charge = stripe.Charge.create(
      amount=2000,
      currency="aud",
      source="tok_mastercard", # obtained with Stripe.js
      metadata={'order_id': '6735'}
    )
    print(charge)
    return HttpResponse(charge)
