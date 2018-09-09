from django.db import models
from django.conf import settings

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
    tags = models.ForeignKey('ProductTags',
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


class ProductTags(models.Model):
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
