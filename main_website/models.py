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
