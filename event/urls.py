from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import index, credit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('credit/', credit, name='credit'),
    path('organisateur/', include('organisator.urls')),
    path('participant/', include('participant.urls')),
    path('evenement/', include('evenement.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()