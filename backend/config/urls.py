from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    url(r'admin/', admin.site.urls),
]

# urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
