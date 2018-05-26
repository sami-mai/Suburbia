from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Suburb(models.Model):
    """
    Model for a suburb
    """
    name = models.CharField(max_length=200)
    location = models.PointField()

    def __str__(self):
        return self.name


class Residents(models.Model):
    user = models.ForeignKey(User, related_name='user_suburb')
    suburb = models.ForeignKey(Suburb, related_name="residency")

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("suburb", "user")
