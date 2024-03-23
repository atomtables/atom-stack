import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import blogsite.models

def random_pfp(p1, p2):
    return f"profile_pictures/{random.getrandbits(128)}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(
        blank=True,
        upload_to=random_pfp,
        default="profile_pictures/user_pfp.png"
    )
    last_visit = models.DateTimeField(blank=True, null=True)
    user_blog_comments = models.ManyToManyField(blogsite.models.Comment, blank=True, related_name='user_blog_comments')
    user_blog_posts = models.ManyToManyField(blogsite.models.BlogPost, blank=True, related_name='user_blog_posts')
    user_blog_likes = models.ManyToManyField(blogsite.models.BlogPost, blank=True, related_name='user_blog_likes')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
