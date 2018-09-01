from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.
class Membership(models.Model):
    MEMBERSHIP_OPTIONS = (
        ('0', 'Regular'),
        ('1', 'Cancelled'),
        ('2', 'Admin'),
    )
    Membership_num = models.AutoField(primary_key=True)
    Membership_type = models.CharField(choices=MEMBERSHIP_OPTIONS, max_length=1)
    Start_date = models.DateField(blank=True,null=True)
    End_date = models.DateField(blank=True,null=True)
    Paid = models.BooleanField(default=False)

class Maintenance(models.Model):

    MAINTENANCE_OPTIONS = (
        ('0', 'Ok'),
        ('1', 'At Repairer'),
        ('2', 'With Staff Member'),
    )
    Maintenance_id = models.AutoField(primary_key=True)
    Maintenance_status = models.CharField(choices=MAINTENANCE_OPTIONS, max_length=1)
    Maintenance_location = models.CharField(max_length=255)
    Maintenance_notes = models.TextField(blank=True, null=True)

class Contact(models.Model):
    LANGUAGE_OPTIONS =(
        ('0', 'English'),
    )
    Contact_id = models.AutoField(primary_key=True)
    First_name = models.CharField(max_length=30)
    Last_name = models.CharField(max_length=30)
    Address = models.CharField(max_length=200)
    Email = models.EmailField(max_length=70, null=True, blank=True, unique=True)
    Telephone_num = models.IntegerField()
    Postcode = models.IntegerField()
    City = models.CharField(max_length=20)
    County = models.CharField(max_length=50)
    Preferred_language = models.CharField(choices=LANGUAGE_OPTIONS, max_length=1)
    Account_balance = models.FloatField()
    Maillist = models.BooleanField(default=False)
    Password = models.CharField(max_length=128)
    Membership_num = models.ForeignKey(Membership, on_delete=models.CASCADE)
