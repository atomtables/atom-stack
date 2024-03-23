from django.contrib import admin

from blogsite.models import Comment, BlogPost, BlogImage

# Register your models here.
admin.site.register(Comment)
admin.site.register(BlogPost)
admin.site.register(BlogImage)