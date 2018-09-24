from django.contrib import admin
from .models import Product, ProductImage, ProductType, ProductTag, \
    ProductLocation, ProductCondition, Cart, User, Member, Lending, \
    LendingHistory, OpeningHour, UserImage
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import UserCreationForm, UserChangeForm

@admin.register(User)
class UserAdmin(UserAdmin):
    """Display list of users for admin dashboard"""
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
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'get_member')
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


class UserImageInline(admin.TabularInline):
    """Display list of images for a user admin dashboard"""
    model = UserImage
    readonly_fields = ('image_tag',)

    def image_tag(self,obj):
        """Display te actual image with 200x200 pixel size"""
        width='200px'
        height='200px'
        return mark_safe(
            '<img src="{}" width={} height={}/>'.format(obj.image.url,
                                                        width, height))

class UserImageAdmin(admin.ModelAdmin):
    """Display list of images for admin dashboard"""
    list_display = ('user', 'alt')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return mark_safe('<img src="{}" />'.format(obj.image.url))

class MemberAdmin(admin.ModelAdmin):
    """Display list of members for admin dashboard"""
    model = Member

    list_display = ('get_email', 'membership_type', 'start_time',
                    'end_time')
    #search_fields = ('user_id', 'get_email', 'membership_type')
    ordering = ('user_id', 'membership_type', 'start_time',
                'end_time')

    def get_email(self,obj):
        return obj.user.email
    get_email.short_description = "Email"
    get_email.admin_order_field = 'user__email'


class ProductImageInline(admin.TabularInline):
    """Display list of images for a product admin dashboard"""
    model = ProductImage
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        """Display the actual image with 200x200 pixel size"""
        width='200px'
        height='200px'
        return mark_safe(
        '<img src="{}" width={} height={}/>'.format(obj.image.url,
                                                    width, height))


class ProductAdmin(admin.ModelAdmin):
    """Display list of products for admin dashboard"""
    list_display = ('name', 'code', 'loan_period',)
    inlines = [ProductImageInline]


class ProductImageAdmin(admin.ModelAdmin):
    """Display list of images for admin dashboard"""
    list_display = ('product', 'alt')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return mark_safe('<img src="{}" />'.format(obj.image.url))


class ProductTypeAdmin(admin.ModelAdmin):
    """Display list of product type for admin dashboard"""
    list_display = ('type_name',)


class ProductTagAdmin(admin.ModelAdmin):
    """Display list of product tag for admin dashboard"""
    list_display = ('tag_name',)


class ProductLocationAdmin(admin.ModelAdmin):
    """Display list of product location for admin dashboard"""
    list_display = ('location_name',)


class ProductConditionAdmin(admin.ModelAdmin):
    """Display list of product condition for admin dashboard"""
    list_display = ('condition_name',)


class CartAdmin(admin.ModelAdmin):
    """Display list of cart for admin dashboard"""
    list_display = ('user_id', 'item')


class LendingAdmin(admin.ModelAdmin):
    """Display list of lendings for admin dashboard"""
    list_display = ('productId', 'userId', 'startDate',
                    'endDate', 'productStatus')
    list_editable = ('productStatus',)

class LendingHistoryAdmin(admin.ModelAdmin):
    """Display list of lending histories for admin dashboard"""
    list_display = ('productId', 'userId', 'startDate',
                    'endDate', 'productStatus')
    list_editable = ('productStatus',)


class OpeningHourAdmin(admin.ModelAdmin):
    """Display list of product tag for admin dashboard"""
    list_display = ('opening_date',)


"""Register all the admin view"""
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(ProductLocation, ProductLocationAdmin)
admin.site.register(ProductCondition, ProductConditionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Lending, LendingAdmin)
admin.site.register(LendingHistory, LendingHistoryAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)
admin.site.register(UserImage, UserImageAdmin)

"""Set admin header and title"""
admin.site.site_header = "Share Shed Admin"
admin.site.site_title = "Share Shed admin login"
admin.site.index_title = "Hello"
