from django.contrib import admin
from .models import Product, ProductImage, ProductType, ProductTags, \
    ProductLocation, ProductCondition, Cart
from django.utils.html import mark_safe

# Register your models here.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        width='200px'
        height='200px'
        return mark_safe('<img src="{}" width={} height={}/>'.format(obj.image.url, width, height))


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'loan_period',)
    inlines = [ProductImageInline]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return mark_safe('<img src="{}" />'.format(obj.image.url))


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
