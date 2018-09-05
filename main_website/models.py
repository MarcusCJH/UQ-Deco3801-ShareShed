from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    membership_options = (
        ('g', 'Guest'),
        ('r', 'Regular'),
        ('l', 'Librarian'),
    )
    membership = models.CharField(choices=membership_options, max_length=1, default='g')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class User(models.Model):
    contact_id = models.AutoField(primary_key=True)
    member_id = models.IntegerField(unique=True)
    added_on = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    membership = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
    )
    email = models.EmailField(unique=True)
    subscriber = models.BooleanField(default=True)
    telephone = models.CharField(max_length=15)
    street = models.TextField()
    city = models.CharField(max_length=30)
    county = models.CharField(max_length=30)
    postcode = models.CharField(max_length=4)
    country = models.CharField(max_length=30)
    balance = models.FloatField()
    suburb = models.CharField(max_length=30)
