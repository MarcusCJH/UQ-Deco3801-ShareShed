from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
import datetime

# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


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


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    maillist = models.BooleanField(default=True)
    telephone_num = models.CharField(_('Telephone Number'), max_length=15)
    address = models.TextField(max_length=30)
    city = models.CharField(max_length=20)
    county = models.CharField(max_length=30)
    postcode = models.CharField(max_length=4)
    country = models.CharField(max_length=30)
    balance = models.FloatField(default=0)
    suburb = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, **kwargs):
        super(User, self).save(**kwargs)
        member = Member(user=self)
        if self.is_staff:
            member.membership_type = 'l'
        else:
            member.membership_type = 'g'
        member.save()

class Member(models.Model):
    user = models.OneToOneField(
        User,
        related_name='membership',
        primary_key=True,
        on_delete=models.CASCADE,
    )
    membership_options = (
        ('g', 'Guest'),
        ('r', 'Regular'),
        ('l', 'Librarian'),
    )
    membership_type = models.CharField(choices=membership_options, max_length=1)
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)

