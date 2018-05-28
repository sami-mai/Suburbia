from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Lookup
    # url(r'^$', LookupView.as_view(), name='lookup'),  (?P<username>[-\w]+)/
    url(r'^(\d+)/$', views.edit_profile, name='edit_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
