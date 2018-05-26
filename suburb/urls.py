from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import LookupView

urlpatterns = [
    # Lookup
    url(r'^$', LookupView.as_view(), name='lookup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
