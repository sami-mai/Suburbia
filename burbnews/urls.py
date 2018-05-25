from django.conf.urls import url
from . import views as news_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^news/(\d+)', news_views.home, name='news_home'),
    # url(r'^edit-profile/(\d+)', news_views.edit_profile, name='edit_userprofile'),
]


# configure our urls.py to register the MEDIA_ROOT route.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
