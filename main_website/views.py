from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from .tokens import account_activation_token
from .models import User, Member, Payment, ProductCategory, Product, \
    ProductImage, OpeningDay
from .forms import UserCreationForm, IdentificationForm, UserChangeForm, \
    OrderNoteForm, ItemLendForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import stripe
import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY

def homepage(request):
    categories = ProductCategory.objects.all()[:11]
    context = {
        'categories': categories,
    }
    return render(request, 'home.html', context)


def catalogue(request, category_id='0', availability_id='0'):
    categories = ProductCategory.objects.all().annotate(
        num_count=Count('product'))
    current_category = ''

    if category_id == '0':
        if availability_id == '0':
            products = Product.objects.all()
        elif availability_id == '1':
            products = Product.objects.filter(shown=True)
        available_products = Product.objects.filter(shown=True)
        whole_products = Product.objects.all()

    else:
        if availability_id == '0':
            products = Product.objects.filter(category=category_id)
        elif availability_id == '1':
            products = Product.objects.filter(category=category_id, shown=True)
        available_products = Product.objects.filter(shown=True, category=category_id)
        whole_products = Product.objects.filter(category=category_id)
        current_category = ProductCategory.objects.get(id = category_id)

    products_images = ProductImage.objects.all()

    return render(request, 'catalogue/catalogue.html',
                  {'categories': categories, 'products': products,
                  'available_products': available_products,
                  'whole_products': whole_products,
                  'category_id': category_id,
                  'availability_id': availability_id,
                  'products_images': products_images,
                  'current_category': current_category})


def item_details(request, product_id):
        products = Product.objects.get(id=product_id)
        images = ProductImage.objects.filter(product_id=product_id)
        current_user = request.user
        message = ''

        if request.method == 'POST':
            if (current_user.balance - products.fee >= 0):
                form = ItemLendForm(request.POST)
                form.instance.product = products
                form.instance.user = current_user
                if form.is_valid():
                    if request.session.get('action') == "CONFIRMED":
                        lending = form.save(commit=False)
                        lending.product_status = 'RESERVED'
                        current_user.balance -= products.fee
                        lending.save()
                        current_user.save()
                        request.session['action'] = "UNCONFIRMED"

                        start_day = int(form.instance.start_date.strftime('%w')) - 1
                        if start_day < 0:
                            start_day = 6
                        start_hours = OpeningDay.objects.get(opening_day=start_day).opening_hour
                        start_hours = (datetime.datetime.combine(datetime.date(1,1,1),start_hours) + datetime.timedelta(hours=1)).time()
                        mail_subject = 'Share Shed Borrowing Summary'
                        message = render_to_string('catalogue/email_summary.html', {
                            'user': current_user,
                            'products': products,
                            'start_date': form.instance.start_date,
                            'start_hours': start_hours,
                            'lending': lending,
                            'images': images
                        })
                        to_email = current_user.email
                        send_mail(mail_subject,
                                  message,
                                  settings.EMAIL_HOST_USER,
                                  [to_email],
                                  fail_silently=False)

                        return redirect('/loan_success')
                    else:
                        request.session['action'] = "CONFIRMED"
                        start_day = int(form.instance.start_date.strftime('%w')) - 1
                        if start_day < 0:
                            start_day = 6
                        return_day = int(form.instance.end_date.strftime('%w')) - 1
                        if return_day < 0:
                            return_day = 6
                        start_hours = OpeningDay.objects.get(opening_day=start_day).opening_hour
                        start_hours = (datetime.datetime.combine(datetime.date(1,1,1),start_hours) + datetime.timedelta(hours=1)).time()
                        return_hours = OpeningDay.objects.get(opening_day=return_day).opening_hour
                        context = {
                        'products': products,
                        'form': form,
                        'start_hours': start_hours,
                        'return_hours': return_hours,
                        'images': images
                        }
                        return render(request, 'catalogue/summary.html', context)

            else:
                form = ItemLendForm(request.POST)
                message = "You don't have the balance to borrow this item. Please top up first."
        else:
            form = ItemLendForm()
        request.session['action'] = "UNCONFIRMED"
        context = {
            "products": products,
            'form': form,
            'message': message,
            'images': images
        }
        return render(request, 'catalogue/item-details.html', context)




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


@login_required
def update_profile(request):
    if not request.user.is_authenticated:
        return redirect()
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {
        'form': form,
    })


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
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [to_email],
                      fail_silently=False)
            return render(request, 'user/activate.html',
                          {'recipient': to_email})
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def resend_email_activation(request):
    if request.method == 'POST':
        recipient = request.POST.get("recipient", "")
        user = User.objects.get(email=recipient)
        current_site = get_current_site(request)
        mail_subject = 'Share Shed Email Activation'
        message = render_to_string('registration/email_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
        })
        to_email = recipient
        send_mail(mail_subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [to_email],
                  fail_silently=False)

        return render(request, 'user/activate.html', {'recipient': to_email})
    return render(request, 'user/activate.html', {'recipient': recipient})


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


@login_required
def upload_identification(request):
    current_user = request.user
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


@login_required
def membership_renew(request):
    """Method to renew membership"""
    current_user = request.user

    if request.method == 'POST':
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

            payment = Payment(user_id=current_user.id,
                              stripe_payment_id=charge.id,
                              stripe_payment_date=datetime.datetime
                              .fromtimestamp(charge.created)
                              .strftime('%Y-%m-%d %H:%M:%S'),
                              amount=(charge.amount/100))
            print(payment)
            payment.save()

        # ENDPAYMENT
        member = Member.objects.get(user_id=current_user.id)
        if member.start_time is None and member.end_time is None:
            member.membership_type = "m"
            member.start_time = timezone.now()
            member.end_time = member.start_time + relativedelta(years=1)

        elif (member.end_time):
            member.end_time = member.end_time + relativedelta(years=1)

        member.save()

        current_site = get_current_site(request)
        mail_subject = 'Membership Purchase'
        message = render_to_string('registration/email_activation.html', {
            'user': current_user,
            'membership_end': member.end_time
        })
        to_email = current_user.email
        send_mail(mail_subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [to_email],
                  fail_silently=False)
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

            # Logic for payment balance
            user = User.objects.get(id=current_user.id)
            user.balance = user.balance + (charge.amount/100)
            user.save()
        # ENDPAYMENT
    return redirect('profile')


@login_required
def profile(request):
    return render(request, 'user/profile.html')
