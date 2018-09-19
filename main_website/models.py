from django.db import models

from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import datetime

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
        ('m', 'Member'),
        ('l', 'Librarian'),
    )
    membership_type = models.CharField(choices=membership_options, max_length=1)
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)


def validate_date(value):
    if value.weekday() in [1,2,3,6]:
        raise ValidationError(
            ('Share Shed is not open'),
        )


    expirydate = '2018-09-30'
    expiry = datetime.strptime(expirydate, '%Y-%m-%d').date()
    if value >expiry:
        raise ValidationError(
            ('Please borrow within membership period'),
        )
    dateList = []
    fridate = '2018-09-14'
    friexpiry = datetime.strptime(fridate, '%Y-%m-%d').date()
    satdate = '2018-09-15'
    satexpiry = datetime.strptime(satdate, '%Y-%m-%d').date()
    mondate = '2018-09-17'
    monexpiry = datetime.strptime(mondate, '%Y-%m-%d').date()
    dateList.append(friexpiry)
    dateList.append(satexpiry)
    dateList.append(monexpiry)
    if value not in dateList:
        raise ValidationError(
            ('Sorry we are closed.'),
        )


class Product(models.Model):
    name = models.CharField(max_length=128)
    long_description = models.TextField()
    short_description = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    available_on = models.DateField(blank=True, null=True)
    shown = models.BooleanField(default=True)
    added_on = models.DateField(blank=True, null=True, auto_now_add=True)
    code = models.CharField(max_length=8)
    brand = models.CharField(max_length=32)
    price_paid = models.DecimalField(max_digits=8, decimal_places=2)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    loan_period = models.IntegerField()
    components = models.TextField()
    care_information = models.TextField()
    keywords = models.CharField(max_length=128)
    type = models.ForeignKey('ProductType',
        null=True, on_delete=models.SET_NULL)
    tags = models.ForeignKey('ProductTag',
        null=True, on_delete=models.SET_NULL)
    location = models.ForeignKey('ProductLocation',
        null=True, on_delete=models.SET_NULL)
    condition = models.ForeignKey('ProductCondition',
        null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images',
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', blank=False)
    alt = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return str(self.alt)


class ProductType(models.Model):
    type_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.type_name)


class ProductTag(models.Model):
    tag_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.tag_name)


class ProductCondition(models.Model):
    condition_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.condition_name)


class ProductLocation(models.Model):
    location_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.location_name)


class Cart(models.Model):
    item = models.ForeignKey('Product',
        null=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item)


class Payment(models.Model):
    id = models.IntegerField
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    stripe_payment_id = models.CharField(max_length=27, blank=True, null=True)
    stripe_payment_date = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
class Lending(models.Model):
    productId = models.ForeignKey('Product', null=False, on_delete=models.PROTECT)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=False, on_delete=models.CASCADE)
    startDate = models.DateField(validators=[validate_date])
    endDate = models.DateField(validators=[validate_date])

    productStatusChoices = (
        ('ONLOAN', 'ON LOAN'),
        ('RETURNTODAY','RETURN TODAY'),
        ('RETURNLATE', 'RETURN LATE'),
        ('RESERVED','RESERVED'),
        ('COLLECTTODAY','COLLECT TODAY'),
        ('COLLECTLATE','COLLECT LATE'),
    )

    productStatus = models.CharField(
        max_length=12,
        choices=productStatusChoices,
        null=False,
    )

    def duration(self):
        duration = self.startDate - self.endDate
        return str(duration)

    def __str__(self):
        name = self.productId.name
        return str(name)

class LendingHistory(models.Model):
    productId = models.ForeignKey('Product', null=False, on_delete=models.PROTECT)
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=False, on_delete=models.CASCADE)
    startDate = models.DateField(validators=[validate_date])
    endDate = models.DateField(validators=[validate_date])

    productStatusChoices = (
        ('ONLOAN', 'ON LOAN'),
        ('RETURNTODAY','RETURN TODAY'),
        ('RETURNLATE', 'RETURN LATE'),
        ('RESERVED','RESERVED'),
        ('COLLECTTODAY','COLLECT TODAY'),
        ('COLLECTLATE','COLLECT LATE'),
    )

    productStatus = models.CharField(
        max_length=12,
        choices=productStatusChoices,
        null=False,
    )

    def duration(self):
        duration = self.startDate - self.endDate
        return str(duration)

    def __str__(self):
        name = self.productId.name
        return str(name)
