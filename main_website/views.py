from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta
import datetime

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
