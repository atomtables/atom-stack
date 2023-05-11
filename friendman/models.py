from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class FriendMessageData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_requests = models.JSONField(default=list, blank=True)
    friends = models.JSONField(default=list, blank=True)


@receiver(post_save, sender=User)
def create_user_friend_message_data(sender, instance, created, **kwargs):
    if created:
        FriendMessageData.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_friend_message_data(sender, instance, **kwargs):
    instance.profile.save()
