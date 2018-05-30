from django.contrib import admin
from . import models


class TopicMemberInline(admin.TabularInline):
    model = models.TopicMember


admin.site.register(models.Topic)
admin.site.register(models.TopicMember)
admin.site.register(models.Post)
