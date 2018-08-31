from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=15)
    code = models.CharField(max_length=10, primary_key=True)

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class Semester(models.Model):
    semester_options=(
        ('1', 'Odd'),
        ('2', 'Even'),
    )
    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    semester_type = models.CharField(choices=semester_options, max_length=1)
    courses = models.ManyToManyField(Course)


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
    Maintenance_location = models.CharField(max_length=255)
    Maintenance_notes = models.TextField(blank=True, null=True)

