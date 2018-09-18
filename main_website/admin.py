from django.contrib import admin
from .models import Product, ProductImage, ProductType, ProductTag, \
    ProductLocation, ProductCondition, Cart, User, Member
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(UserAdmin):
    member = Member('user_id')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'telephone_num', 'address', 'city',
                                         'county', 'postcode', 'country',
                                         'suburb', 'balance')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name',
                       'last_name', 'telephone_num', 'address', 'city',
                       'county', 'postcode', 'country', 'suburb'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'get_member')
    search_fields = ('email', 'first_name', 'last_name', 'telephone_num',
                     'address', 'city', 'county', 'postcode', 'country',
                     'suburb')
    ordering = ('email',)

    def get_member(self, obj):
        member = Member.objects.get(user_id=obj.id)
        membership_options = {
            'g': 'Guest',
            'm': 'Member',
            'l': 'Librarian'
        }
        return membership_options[member.membership_type]
    get_member.short_description = "Member"


class MemberAdmin(admin.ModelAdmin):
    model = Member

    list_display = ('get_email', 'membership_type', 'start_time',
                    'end_time')
    search_fields = ('user_id', 'get_email', 'membership_type')
    ordering = ('user_id', 'membership_type', 'start_time',
                'end_time')

    def get_email(self,obj):
        return obj.user.email
    get_email.short_description = "Email"
    get_email.admin_order_field = 'user__email'

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
admin.site.register(Member, MemberAdmin)
admin.site.site_header = "Share Shed Admin"
admin.site.site_title = "Share Shed admin login"
admin.site.index_title = "Hello"