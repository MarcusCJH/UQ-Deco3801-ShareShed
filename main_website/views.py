from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib import messages
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def louis(request, random_number):
    return HttpResponse("Hello, world. " + str(random_number))

def risyad(request, random_number):
    return HttpResponse("Hello, world. " + str(random_number))

@csrf_exempt
def checkout(request):
    if request.method == "POST":
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=8000,
                currency="aud",
                source=token,
                description="The product charged to the user",
                receipt_email=request.POST['stripeEmail'],
            )

            print(request.POST['stripeEmail'])
            print(token)
            print(charge)


            #subscription = stripe.Subscription.create(
            #    customer="cus_DaMnpxcZSGJY1y",
            #    items=[
            #        {
            #            "plan": "plan_DYkJBVyTAFAbx8",
            #            "quantity": 1,
            #        },
            #    ],
            #    billing='send_invoice',
            #   days_until_due=30,
            #)



            messages.info(request, "Payment is successful")
        except stripe.error.CardError as ce:
            return False, ce

    context = {"stripe_key": settings.STRIPE_PUBLISHABLE_KEY}
    return render(request,'paymentsystest/test.html',context)

