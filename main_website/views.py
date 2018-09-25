import datetime
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from .tokens import account_activation_token
from .models import User, Member, Payment
from .forms import UserCreationForm, IdentificationForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def sign_up(request):
    """Method to invoke user sign up form."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Share Shed Email Activation'
            message = render_to_string('registration/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False)
            return render(request, 'user/activate.html')
            # return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

def upload_identification(request):
    current_user = request.user;
    if request.method == 'POST':
        form = IdentificationForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            image = form.save(commit=False)
            image.user_id = current_user.id
            image.save()
            return redirect('/profile')
    else:
        form = IdentificationForm()
    return render(request, 'user/idupload.html', {'form': form})

def membership_renew(request):
    """Method to renew membership"""
    current_user = request.user

    if request.method == 'POST':

        #TEST EMAIL HERE
        #TODO: Seems like there's a problem sending email
        #send_mail('Subject here',
        #    'Here is the message.',
        #   settings.EMAIL_HOST_USER,
        #    ['shareshed@risyad.cloud'],
        #    fail_silently=False)

        # PAYMENT
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=8000,
                currency="aud",
                source=token,
                description="The product charged to the user",
                receipt_email=request.POST['stripeEmail'],
            )
        except stripe.error.CardError as ce:
            return False, ce
        else:
            '''If charge was successful
            TODO: RuntimeWarning: DateTimeField
            received a naive datetime _____ while time zone support is active.
            Not sure if this is an issue'''

            payment = Payment(user_id = current_user.id,
                                stripe_payment_id=charge.id,
                                stripe_payment_date=datetime.datetime
                                .fromtimestamp(charge.created)
                                .strftime('%Y-%m-%d %H:%M:%S'),
                                amount=(charge.amount/100))
            payment.save()

        # ENDPAYMENT
        member = Member.objects.get(user_id=current_user.id)
        if member.start_time == None and member.end_time == None:
            member.membership_type = "m"
            member.start_time = timezone.now()
            member.end_time = member.start_time + relativedelta(years=1)


        elif (member.end_time):
            member.end_time = member.end_time + relativedelta(years=1)

        member.save()



    return redirect('profile')

@csrf_exempt
def top_up_credit(request):
    """Payment for credits"""
    current_user = request.user
    if request.method == 'POST':
        # PAYMENT
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=request.POST['amountInCents'],
                currency="aud",
                source=token,
                description="The product charged to the user",
                receipt_email=request.POST['stripeEmail'],
            )
        except stripe.error.CardError as ce:
            return False, ce
        else:
            '''If charge was successful
            TODO: RuntimeWarning: DateTimeField
            received a naive datetime _____ while time zone support is active.
            Not sure if this is an issue'''

            payment = Payment(user_id=current_user.id,
                              stripe_payment_id=charge.id,
                              stripe_payment_date=datetime.datetime
                              .fromtimestamp(charge.created)
                              .strftime('%Y-%m-%d %H:%M:%S'),
                              amount=(charge.amount / 100))
            payment.save()

            #Logic for payment balance
            user = User.objects.get(id=current_user.id)
            user.balance = user.balance + (charge.amount/100)
            user.save()
        # ENDPAYMENT
    return redirect('profile')

def test_email(request):
    success = send_mail('Test mail',
                        'Hello',
                        settings.EMAIL_HOST_USER,
                        ['risyadhasbullah@gmail.com'],
                        fail_silently=False)

    if success:
        return HttpResponse('Success')
    else:
        return HttpResponse('Invalid')
