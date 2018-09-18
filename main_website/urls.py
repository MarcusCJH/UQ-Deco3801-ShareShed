from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.success, name='success'),
    url(r'^signup/$', views.SignUp , name='signup'),
    url(r'^membership/$',views.membershipRenew, name='membership')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)