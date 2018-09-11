from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.index, name='homepage'),
    path('testing/<int:random_number>', views.louis, name='dynamic_web'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
