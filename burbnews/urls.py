from django.conf.urls import url
from . import views as news_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # url(r'^(\d+)', news_views.home, name='news_home'),
    url(r'^topics/$', news_views.ListTopics.as_view(), name="all_topics"),
    url(r'^topics/new_topic/$', news_views.CreateTopic.as_view(), name="create_topic"),
    url(r'^topics/posts/in/(?P<slug>[-\w]+)/$', news_views.SingleTopic.as_view(), name="single_topic"),
    url(r'^topics/join/(?P<slug>[-\w]+)/$', news_views.JoinTopic.as_view(), name="join_topic"),
    url(r'^topics/leave/(?P<slug>[-\w]+)/$', news_views.LeaveTopic.as_view(), name="leave_topic"),

    url(r'^posts/$', news_views.PostList.as_view(), name="all_posts"),
    url(r'^posts/new_post/$', news_views.CreatePost.as_view(), name="create_post"),
    url(r'^posts/by/(?P<username>[-\w]+)/$', news_views.UserPosts.as_view(), name="for_user"),
    url(r'^posts/by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', news_views.PostDetail.as_view(), name="single_post"),
    url(r'^posts/delete/(?P<pk>\d+)/$', news_views.DeletePost.as_view(), name="delete_post"),

]


# configure our urls.py to register the MEDIA_ROOT route.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
