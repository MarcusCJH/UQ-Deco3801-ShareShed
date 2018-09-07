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
    membership_type = models.CharField(choices=membership_options, max_length=1, default='g')
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)

    @classmethod
    def get_new(cls):
        return cls.objects.create().id

class Maintenance(models.Model):

    MAINTENANCE_OPTIONS = (
        ('0', 'Ok'),
        ('1', 'At Repairer'),
        ('2', 'With Staff Member'),
    )
    maintenance_id = models.AutoField(primary_key=True)
    maintenance_status = models.CharField(choices=MAINTENANCE_OPTIONS, max_length=1)
    maintenance_location = models.CharField(max_length=255)
    maintenance_notes = models.TextField(blank=True, null=True)


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
    maillist = models.BooleanField(default=True)
    telephone_num = models.CharField(max_length=15)
    address = models.TextField(max_length=30)
    city = models.CharField(max_length=20)
    county = models.CharField(max_length=50)
    postcode = models.CharField(max_length=4)
    country = models.CharField(max_length=30)
    balance = models.FloatField(default=0)
    suburb = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
