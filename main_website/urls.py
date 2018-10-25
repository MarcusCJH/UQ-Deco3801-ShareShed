from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

'''Contains all the url pattern and redirect to corresponding action'''
urlpatterns = [
    path('', views.homepage, name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('catalogue/<category_id>/', views.catalogue, name='catalogue'),
    path('catalogue/<category_id>/<availability_id>', views.catalogue, name='catalogue'),
    path('item/<product_id>', views.item_details, name='item_details'),
    path('item/',
         TemplateView.as_view(template_name='catalogue/item-details.html')),
    path('signup/', views.sign_up, name='signup'),
    path('signup/resend_email_activation/',
         views.resend_email_activation, name='resend_email_activation'),
    path('membership', views.membership_renew, name='membership'),
    path('topup', views.top_up_credit, name='topup'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.update_profile, name='update_profile'),
    path('profile/change_password', views.change_password,
         name='change_password'),
    path('profile/idupload', views.upload_identification,
         name='upload_identification'),
    path('loan_success',
         TemplateView.as_view(template_name='catalogue/success.html')),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/'
            '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.user_activation, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
