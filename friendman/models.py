from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_requests = models.JSONField(default=list, blank=True)
    friends = models.JSONField(default=list, blank=True)


@receiver(post_save, sender=User)
def create_user_friend(sender, instance, created, **kwargs):
    if created:
        Friend.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_friend(sender, instance, **kwargs):
    instance.profile.save()
