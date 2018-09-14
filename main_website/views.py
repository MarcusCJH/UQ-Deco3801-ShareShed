from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from dateutil.relativedelta import relativedelta
import stripe
import datetime
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import User, Member

from .forms import UserCreationForm

def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def membershipRenew(request):
    current_user = request.user
    if request.method == 'POST' :
        member = Member.objects.get(user_id=current_user.id)
        if member.start_time == None and member.end_time == None:
            member.membership_type = "m"
            member.start_time = datetime.datetime.now()
            member.end_time = member.start_time + relativedelta(years=1)
        elif (member.end_time):
            member.end_time = member.end_time + relativedelta(years=1)
        member.save()
    return redirect('home')


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

            if charge.paid is True:
                return redirect('success')

        except stripe.error.CardError as ce:
            return False, ce

    context = {"stripe_key": settings.STRIPE_PUBLISHABLE_KEY}
    return render(request,'paymentsystest/index.html',context)

def success(request):
    return render(request, 'paymentsystest/success.html')
