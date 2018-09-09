from django.contrib import admin
from .models import Product, ProductImage, ProductType, ProductTags, \
    ProductLocation, ProductCondition, Cart

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'loan_period')


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt')


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)


class ProductTagsAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)


class ProductLocationAdmin(admin.ModelAdmin):
    list_display = ('location_name',)


class ProductConditionAdmin(admin.ModelAdmin):
    list_display = ('condition_name',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'item')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductTags, ProductTagsAdmin)
admin.site.register(ProductLocation, ProductLocationAdmin)
admin.site.register(ProductCondition, ProductConditionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.site_header = "Share Shed Admin"
admin.site.site_title = "Share Shed admin login"
admin.site.index_title = "Hello"
