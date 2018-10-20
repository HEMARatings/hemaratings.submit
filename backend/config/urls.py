from django.conf.urls import url
from django.contrib import admin

from submit.views import index

urlpatterns = [url(r"admin/", admin.site.urls), url(r"", index, name="index")]

# urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
