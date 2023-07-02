import time
from hashlib import sha256

from django.contrib.auth.models import User
from ninja import NinjaAPI

from friendman.models import FriendRequestRelationship, FriendRelationship

api = NinjaAPI()


class UserAuthException(Exception):
    pass


@api.exception_handler(UserAuthException)
def user_no_auth(request, exc):
    return api.create_response(
        request,
        {"error": "You are not authorized to access this page, either due to not being logged in or "
                  "not having the correct permissions.", "code": 403},
        status=403,
    )


@api.get("/frq/{username}")
def request_friend(request, username: str):
    if not request.user.is_authenticated:
        raise UserAuthException()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return api.create_response(
            request,
            {"error": "User does not exist", "code": 100},
            status=404,
        )
    if user is not None:
        print(user.friend.friend_requests.all())
        for u in user.friend.friend_requests.all():
            if u.outgoing_friend.username == request.user.username \
                    or u.incoming_friend.username == request.user.username:
                return api.create_response(
                    request,
                    {"error": "There is already an active friend request between these 2 users", "code": 101},
                    status=400,
                )
        for u in user.friend.friends.all():
            if u.friend1.username == request.user.username or u.friend2.username == request.user.username:
                return api.create_response(
                    request,
                    {"error": "There is already a friendship between these 2 users", "code": 102},
                    status=400,
                )
        FriendRequestRelationship.objects.create(
            outgoing_friend=request.user,
            incoming_friend=user
        )
        return api.create_response(
            request,
            {"success": "Friend request sent"},
            status=200,
        )


@api.get("/fra/{fid}")
def accept_friend_request(request, fid: int):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in request.user.friend.friend_requests.all():
        if x.id == fid:
            if x.incoming_friend.username == request.user.username:
                user = x.outgoing_friend
                FriendRelationship.objects.create(
                    friend1=request.user,
                    friend2=user
                )
                x.delete()
                return api.create_response(
                    request,
                    {"success": "Friend added"},
                    status=200,
                )
            elif x.outgoing_friend.username == request.user.username:
                return api.create_response(
                    request,
                    {"error": "This is not your friend request.", "code": 103},
                    status=403,
                )
    else:
        return api.create_response(
            request,
            {"error": "Friend request not found"},
            status=404,
        )


@api.get("/frd/{fid}")
def decline_friend(request, fid: int):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in request.user.friend.friend_requests.all():
        if x.id == fid:
            if x.incoming_friend.username == request.user.username:
                x.delete()
                return api.create_response(
                    request,
                    {"success": "Friend request declined"},
                    status=200,
                )
            elif x.outgoing_friend.username == request.user.username:
                return api.create_response(
                    request,
                    {"error": "This is not your friend request.", "code": 103},
                    status=403,
                )
    else:
        return api.create_response(
            request,
            {"error": "Friend request not found"},
            status=404,
        )


@api.get("/fd/{fid}")
def remove_friend(request, fid: int):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in request.user.friend.friends.all():
        if x.id == fid:
            if x.friend1.username == request.user.username or x.friend2.username == request.user.username:
                x.delete()
                return api.create_response(
                    request,
                    {"success": "Friend removed"},
                    status=200,
                )
    else:
        return api.create_response(
            request,
            {"error": "Friend request not found"},
            status=404,
        )
