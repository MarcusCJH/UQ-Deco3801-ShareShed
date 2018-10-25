from main_website.models import Lending, OpeningDay
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta
import datetime

def update_lending():
    lendings = Lending.objects.all()
    print("CHECKING")
    for lending in lendings:
        if (lending.product_status == "RESERVED" and date.today() == lending.start_date):
            lending.product_status = "COLLECTTODAY"
            lending.save()
        elif (lending.product_status == "RESERVED" and date.today() + timedelta(days=1) == lending.start_date):
            mail_subject = 'Share Shed Borrow Reminder'
            start_day = int(lending.start_date.strftime('%w')) - 1
            start_hours = OpeningDay.objects.get(opening_day=start_day).opening_hour
            start_hours = (datetime.datetime.combine(datetime.date(1,1,1),start_hours) + datetime.timedelta(hours=1)).time()
            if start_day < 0:
                start_day = 6
            message = render_to_string('scheduling/email_borrowreminder.html', {
                'user': lending.user,
                'products': lending.product,
                'lending': lending,
                'start_date': lending.start_date,
                'start_hours': start_hours
            })
            to_email = lending.user.email
            send_mail(mail_subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [to_email],
                      fail_silently=False)
        elif (lending.product_status == "ONLOAN" and date.today() == lending.end_date):
            lending.product_status = "RETURNTODAY"
            lending.save()
        elif (lending.product_status == "ONLOAN" and date.today() + timedelta(days=1) == lending.end_date):
            mail_subject = 'Share Shed Return Reminder'
            return_day = int(lending.end_date.strftime('%w')) - 1
            return_hours = OpeningDay.objects.get(opening_day=return_day).opening_hour
            if return_day < 0:
                return_day = 6
            message = render_to_string('scheduling/email_returnreminder.html', {
                'user': lending.user,
                'products': lending.product,
                'lending': lending,
                'end_date': lending.end_date,
                'start_hours': return_hours
            })
            to_email = lending.user.email
            send_mail(mail_subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [to_email],
                      fail_silently=False)
        elif (lending.product_status == "RETURNTODAY" and date.today() > lending.end_date):
            mail_subject = 'Share Shed Late Return Notification'
            message = render_to_string('scheduling/email_latereturn.html', {
                'user': lending.user,
                'products': lending.product,
                'lending': lending
            })
            to_email = lending.user.email
            send_mail(mail_subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [to_email],
                      fail_silently=False)
