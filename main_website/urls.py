from django.urls import path
from django.conf.urls import url
from django.views.generic.base import TemplateView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup', views.sign_up , name='signup'),
    path('membership',views.membership_renew, name='membership'),
    path('topup',views.top_up_credit, name='topup'),
    path('profile', TemplateView.as_view(template_name='user/profile.html'),
          name='profile'),
    path('profile/idupload', views.upload_identification, name='upload_identification'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.user_activation, name='activate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
