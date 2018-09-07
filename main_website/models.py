from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
import datetime

# Create your models here.

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    membership_options = (
        ('g', 'Guest'),
        ('r', 'Regular'),
        ('l', 'Librarian'),
    )
    membership = models.CharField(choices=membership_options, max_length=1, default='g')
    start_time = models.DateTimeField('Start',default=datetime.datetime.now)
    end_time = models.DateTimeField('End',default=datetime.datetime.now)

    @classmethod
    def get_new(cls):
        return cls.objects.create().id

class User(models.Model):
    contact_id = models.AutoField(primary_key=True)
    added_on = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    membership = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        default=Member.get_new,
    )
    email = models.EmailField(unique=True)
    subscriber = models.BooleanField(default=True)
    telephone = models.CharField(max_length=15)
    street = models.TextField(max_length=30)
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    postcode = models.CharField(max_length=4)
    country = models.CharField(max_length=30)
    balance = models.FloatField(default=0)
    suburb = models.CharField(max_length=30)
