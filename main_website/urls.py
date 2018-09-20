from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup', views.SignUp , name='signup'),
    path('membership',views.membershipRenew, name='membership'),
    path('topup',views.topupCredit, name='topup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
