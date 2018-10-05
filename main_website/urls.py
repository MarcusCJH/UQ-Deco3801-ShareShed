from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('catalogue/<type_id>/', views.catalogue, name='catalogue'),
    path('catalogue/<type_id>/<product_id>', views.catalogue, name='itemdetail'),
    path('itemdetails/', TemplateView.as_view(template_name='catalogue/itemDetails.html')),
    path('signup/', views.sign_up , name='signup'),
    path('membership',views.membership_renew, name='membership'),
    path('topup',views.top_up_credit, name='topup'),
    path('profile', TemplateView.as_view(template_name='user/profile.html'),
          name='profile'),
    path('profile/edit', views.update_profile, name='update_profile'),
    path('profile/change_password', views.change_password, name='change_password'),
    path('profile/idupload', views.upload_identification, name='upload_identification'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.user_activation, name='activate'),
    path('test_email',views.test_email, name='test_email'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
