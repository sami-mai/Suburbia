from django.contrib.gis.db import models
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# User = get_user_model()


class Suburb(models.Model):
    """
    Model for a suburb
    """
    user = models.OneToOneField(User, related_name='suburb', null=True)
    suburb_name = models.CharField(max_length=200, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)

    def __str__(self):
        return self.name

    # Create Resident Suburb when creating a User
    # @receiver(post_save, sender=User)
    # def create_user_suburb(sender, instance, created, **kwargs):
    #     if created:
    #         Suburb.objects.create(user=instance)
    #     instance.suburb.save()


class Resident(models.Model):
    user = models.OneToOneField(User, related_name='resident', null=True)
    suburb = models.ForeignKey(Suburb, related_name="residency", null=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("suburb", "user")

    # Create Resident Profile when creating a User
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Resident.objects.create(user=instance)
        instance.resident.save()
