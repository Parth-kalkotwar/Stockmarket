from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import urls
from charts import urls as urls3
from newsandcommodities import urls as urls2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(urls)),
    path('commodities/', include(urls2)),
    path('charts/', include(urls3)),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)