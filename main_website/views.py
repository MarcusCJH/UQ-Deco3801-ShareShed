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

    context = {"stripe_key": settings.STRIPE_PUBLISHABLE_KEY}
    return render(request,'paymentsystest/test.html',context)


