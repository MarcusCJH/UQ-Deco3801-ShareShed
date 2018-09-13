from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='homepage'),
    path('testing/<int:random_number>', views.louis, name='dynamic_web'),

    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.success, name='success'),
]
