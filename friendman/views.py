from django.contrib.auth.models import User
from ninja import Router, Schema

from friendman.models import FriendRequestRelationship, FriendRelationship

api = Router()

@api.get("info")
def friend_info(request):
    try:
        if not request.user.is_authenticated:
            return {"error": "You need to be logged in to access.", "code": -2}
        user = request.user
        return {
            "success": "Collected friend information.",
            "code": 2,
            "info": {
                "friends": [x.username for x in user.friend.friends.all()],
                "friend_requests": [x.incoming_friend.username for x in user.friend.friend_requests.all()]
            }
        }
    except:
        return {"error": "Guru Meditation.", "code": -1}

@api.get("add/{username}")
def request_friend(request, username: str):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return {"error": "User does not exist", "code": 100}
    if user is not None:
        print(user.friend.friend_requests.all())
        for u in user.friend.friend_requests.all():
            if u.outgoing_friend.username == request.user.username \
                    or u.incoming_friend.username == request.user.username:
                return {"error": "There is already an active friend request between these 2 users", "code": 101},
        for u in user.friend.friends.all():
            if u.friend1.username == request.user.username or u.friend2.username == request.user.username:
                return {"error": "There is already a friendship between these 2 users", "code": 102},
        FriendRequestRelationship.objects.create(
            outgoing_friend=request.user,
            incoming_friend=user
        )
        return {"success": "Friend request sent"},


@api.get("accept/{fid}")
def accept_friend_request(request, fid: int):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
    for x in request.user.friend.friend_requests.all():
        if x.id == fid:
            if x.incoming_friend.username == request.user.username:
                user = x.outgoing_friend
                FriendRelationship.objects.create(
                    friend1=request.user,
                    friend2=user
                )
                x.delete()
                return {"success": "Friend added"},
            elif x.outgoing_friend.username == request.user.username:
                return {"error": "This is not your friend request.", "code": 103},
    else:
        return {"error": "Friend request not found"},


@api.get("decline/{fid}")
def decline_friend(request, fid: int):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
    for x in request.user.friend.friend_requests.all():
        if x.id == fid:
            if x.incoming_friend.username == request.user.username:
                x.delete()
                return {"success": "Friend request declined"}
            elif x.outgoing_friend.username == request.user.username:
                return {"error": "This is not your friend request.", "code": 103}
    else:
        return {"error": "Friend request not found"}


@api.get("remove/{fid}")
def remove_friend(request, fid: int):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
    for x in request.user.friend.friends.all():
        if x.id == fid:
            if x.friend1.username == request.user.username or x.friend2.username == request.user.username:
                x.delete()
                return {"success": "Friend removed"}
    else:
        return {"error": "Friend request not found"}
