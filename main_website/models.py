from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import datetime

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


# Create your models here.
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

