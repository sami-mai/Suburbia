from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
from suburb.models import Suburb


User = get_user_model()


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through="TopicMember")
    datetime = models.DateTimeField(auto_now=True)
    suburb = models.ForeignKey(Suburb, related_name="local", default='', null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("single_topic", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]


class TopicMember(models.Model):
    topic = models.ForeignKey(Topic, related_name="memberships", null=True)
    user = models.ForeignKey(User, related_name='user_topics', null=True)
    suburb = models.ForeignKey(Suburb, related_name="residents", null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("topic", "user")


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts", null=True)
    image = models.ImageField(upload_to='post_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    topic = models.ForeignKey(Topic, related_name="posts", null=True, blank=True)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "single_post",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]
