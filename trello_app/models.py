from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_token = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user_token

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)