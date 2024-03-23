import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class BlogImage(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    caption = models.CharField(max_length=200, blank=True)
    blog_image_id = models.IntegerField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_content = models.TextField(max_length=500)
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)

class BlogPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500)
    title_image = models.ImageField(upload_to='blog_images/', blank=True)
    title_image_caption = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    comments = models.ManyToManyField(Comment, blank=True)
    blog_images = models.ManyToManyField(BlogImage, blank=True)
    blog_likes = models.ManyToManyField(User, blank=True, related_name='blog_likes')

@receiver(post_save, sender=Comment)
def update_comments(sender, instance, created, **kwargs):
    instance.blog_post.comments.add(instance)
    instance.user.profile.user_blog_comments.add(instance)

@receiver(post_save, sender=BlogPost)
def update_blogpost(sender, instance, created, **kwargs):
    instance.author.profile.user_blog_posts.add(instance)


@receiver(post_save, sender=BlogImage)
def update_blogimage(sender, instance, created, **kwargs):
    instance.blog_post.blog_images.add(instance)