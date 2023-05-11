from django.contrib import admin
from .models import FriendMessageData


# Register your models here.
class FriendManagementAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend_requests', 'friends')


admin.site.register(FriendMessageData, FriendManagementAdmin)
