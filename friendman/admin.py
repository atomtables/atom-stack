from django.contrib import admin
from .models import Friend, FriendRelationship, FriendRequestRelationship


# Register your models here.
class FriendManagementAdmin(admin.ModelAdmin):
    list_display = ('user',)

class FriendRelationshipManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'friend1', 'friend2', 'date_added')


class FriendRequestRelationshipManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'outgoing_friend', 'incoming_friend', 'date_added')


admin.site.register(Friend, FriendManagementAdmin)
admin.site.register(FriendRelationship, FriendRelationshipManagementAdmin)
admin.site.register(FriendRequestRelationship, FriendRequestRelationshipManagementAdmin)
