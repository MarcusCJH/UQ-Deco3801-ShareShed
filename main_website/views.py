from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def louis(request, random_number):
    return HttpResponse("Hello, world. " + str(random_number))

def risyad(request, random_number):
    return HttpResponse("Hello, world. " + str(random_number))


def paymenttest(request):
    return render(request, 'paymentsystest/test.html')

