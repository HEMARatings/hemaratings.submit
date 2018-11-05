from config import settings
from django.conf.urls import url, static
from django.contrib import admin

from submit.views import SubmitWizard, FORMS

urlpatterns = [
    url(r"admin/", admin.site.urls),
    # url(r"", index, name="index"),
    url(r"^$", SubmitWizard.as_view(FORMS)),
]

# urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
