from django.urls import path
from django.views.generic.base import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^signup/$', views.SignUp , name='signup'),
    url(r'^membership/$',views.membershipRenew, name='membership')
]
