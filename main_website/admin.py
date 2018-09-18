from django.contrib import admin
from .models import Product, ProductImage, ProductType, ProductTag, \
    ProductLocation, ProductCondition, Cart, User
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

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


class ProductTagAdmin(admin.ModelAdmin):
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
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(ProductLocation, ProductLocationAdmin)
admin.site.register(ProductCondition, ProductConditionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.site_header = "Share Shed Admin"
admin.site.site_title = "Share Shed admin login"
admin.site.index_title = "Hello"
