from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class FriendRelationship(models.Model):
    friend1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend2')
    date_added = models.DateTimeField(auto_now_add=True)


class FriendRequestRelationship(models.Model):
    outgoing_friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_friend')
    incoming_friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_friend')
    date_added = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_requests = models.ManyToManyField(FriendRequestRelationship, default=list, blank=True)
    friends = models.ManyToManyField(FriendRelationship, default=list, blank=True)


# create and attach a Friend object to every user
@receiver(post_save, sender=User)
def create_user_friend(sender, instance, created, **kwargs):
    if created:
        Friend.objects.create(user=instance)


# save the Friend object every time a user is saved
@receiver(post_save, sender=User)
def save_user_friend(sender, instance, **kwargs):
    instance.profile.save()


# if a friend relationship is created, add it to the Friend object of both users
@receiver(post_save, sender=FriendRelationship)
def update_friend_relationship(sender, instance, created, **kwargs):
    if created:
        instance.friend1.friend.friends.add(instance)
        instance.friend2.friend.friends.add(instance)


# if a friend request relationship is created, add it to the Friend object of both users
@receiver(post_save, sender=FriendRequestRelationship)
def update_friend_request_relationship(sender, instance, created, **kwargs):
    if created:
        instance.outgoing_friend.friend.friend_requests.add(instance)
        instance.incoming_friend.friend.friend_requests.add(instance)
