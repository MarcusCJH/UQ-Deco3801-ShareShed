from django.contrib import admin
from .models import Product, ProductImage, ProductCategory, ProductTag, \
    ProductLocation, ProductCondition, Cart, User, Member, Lending, \
    LendingHistory, OpeningDay, IdentificationImage, OrderNote
from django.utils.html import mark_safe
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import UserCreationForm, UserChangeForm
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.template.response import TemplateResponse


class MyAdminSite(admin.AdminSite):
    """Override the default admin config"""
    @never_cache
    def index(self, request, extra_context=None):
        """Display the main admin index page"""
        lendings = Lending.objects.all()
        collect_today = lendings.filter(Q(product_status='COLLECTTODAY'))
        return_today = lendings.filter(Q(product_status='RETURNTODAY'))
        order_notes = OrderNote.objects.all().order_by('added_on')[::-1][:6]
        today = len(collect_today) + len(return_today)
        reserved = len(lendings.filter(Q(product_status='RESERVED')))
        overdue = len(lendings.filter(Q(product_status='RETURNLATE')))
        onloan = len(lendings.filter(Q(product_status='ONLOAN')))

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'collect_today': collect_today,
            'return_today': return_today,
            'today': today,
            'reserved': reserved,
            'overdue': overdue,
            'onloan': onloan,
            'notes': order_notes,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request,
                                self.index_template or 'admin/index.html',
                                context)


class UserIdentificationInline(admin.StackedInline):
    """Display list of images for a product admin dashboard"""
    model = IdentificationImage
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        """Display the actual image with 200x200 pixel size"""
        width = '200px'
        height = '200px'
        return mark_safe('<img src="{}" width={} height={}/>'
                         .format(obj.image.url, width, height))


class MemberInline(admin.StackedInline):
    """Display list of members for admin dashboard"""
    model = Member

    list_display = ('membership_type', 'start_time',
                    'end_time')
    search_fields = ('user_id', 'get_email', 'membership_type')
    ordering = ('user_id', 'membership_type', 'start_time',
                'end_time')


@admin.register(User)
class UserAdmin(UserAdmin):
    """Display list of users for admin dashboard"""
    member = Member('user_id')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'telephone_num', 'address', 'city',
                                         'suburb', 'state', 'postcode',
                                         'country', 'balance')}),

        (_('Options'), {'fields': ('has_identified', 'has_verified', 'maillist')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name',
                       'last_name', 'telephone_num', 'address', 'city',
                       'suburb', 'state', 'postcode', 'country', 'maillist'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'get_member', 'has_identified')
    search_fields = ('email', 'first_name', 'last_name', 'telephone_num',
                     'address', 'city', 'state', 'postcode', 'country',
                     'suburb')
    ordering = ('first_name',)
    readonly_fields = ('date_joined', 'last_login')
    inlines = [MemberInline, UserIdentificationInline]

    def get_member(self, obj):
        member = Member.objects.get(user_id=obj.id)
        membership_options = {
            'g': 'Guest',
            'm': 'Member',
            'l': 'Librarian'
        }
        return membership_options[member.membership_type]

    get_member.short_description = "Member"

    def get_onloan_count(self):
        number = len(Lending.objects.all().filter(productstatus="ONLOAN"))
        return number


class MemberAdmin(admin.ModelAdmin):
    """Display list of members for admin dashboard"""
    model = Member

    list_display = ('get_email', 'membership_type', 'start_time',
                    'end_time')
    search_fields = ('user_id', 'get_email', 'membership_type')
    ordering = ('user_id', 'membership_type', 'start_time',
                'end_time')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
    get_email.admin_order_field = 'user__email'


class ProductImageInline(admin.TabularInline):
    """Display list of images for a product admin dashboard"""
    model = ProductImage
    readonly_fields = ('image_tag',)
    extra = 0

    def image_tag(self, obj):
        """Display the actual image with 200x200 pixel size"""
        width = '200px'
        height = '200px'
        return mark_safe('<img src="{}" width={} height={}/>'
                         .format(obj.image.url, width, height))


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


class ProductCategoryAdmin(admin.ModelAdmin):
    """Display list of product type for admin dashboard"""
    list_display = ('category_name',)


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
    list_display = ('id', 'product', 'user', 'get_phone', 'get_email', 'get_address', 'start_date',
                    'end_date', 'product_status')
    list_editable = ('product_status',)
    list_filter = ('product_status', )
    search_fields = ('id', 'product__name', 'user__first_name',
                     'user__last_name',)
    date_hierarchy = 'start_date'


    def get_phone(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.telephone_num
    get_phone.short_description = "Phone Number"

    def get_email(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.email
    get_email.short_description = "User Email"

    def get_address(self, obj):
        user = User.objects.get(id=obj.user.id)
        return user.address
    get_address.short_description = "Address"

    def count_status(self, obj):
        number = len(Lending.objects.all().filter(productstatus=obj))
        return number


class LendingHistoryAdmin(admin.ModelAdmin):
    """Display list of lending histories for admin dashboard"""
    list_display = ('product', 'user', 'start_date',
                    'end_date', 'product_status')
    list_filter = ('product_status', )
    search_fields = ('product__name', 'user__first_name',
                     'user__last_name',)
    date_hierarchy = 'start_date'


class OpeningDayAdmin(admin.ModelAdmin):
    """Display list of product tag for admin dashboard"""
    list_display = ('opening_day', 'opening_hour')


class OrderNoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'added_on')


admin_site = MyAdminSite(name='myadmin')

"""Register all the admin view"""
admin_site.register(Product, ProductAdmin)
admin_site.register(ProductImage, ProductImageAdmin)
admin_site.register(ProductCategory, ProductCategoryAdmin)
admin_site.register(ProductTag, ProductTagAdmin)
admin_site.register(ProductLocation, ProductLocationAdmin)
admin_site.register(ProductCondition, ProductConditionAdmin)
admin_site.register(OrderNote, OrderNoteAdmin)
admin_site.register(Cart, CartAdmin)
admin_site.register(Member, MemberAdmin)
admin_site.register(Lending, LendingAdmin)
admin_site.register(LendingHistory, LendingHistoryAdmin)
admin_site.register(OpeningDay, OpeningDayAdmin)

"""Set admin header and title"""
admin_site.site_header = "Share Shed Admin"
admin_site.site_title = "Share Shed admin login"
admin_site.index_title = "Hello"
