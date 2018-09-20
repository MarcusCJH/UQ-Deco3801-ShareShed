from django.urls import path
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
          name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
