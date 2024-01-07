"""
ATOM-STACK API
==================
This API is meant to be used in the development of third-party or first-party apps.
Access will be controlled using an API password later on, however, for development, it is unnecessary.
"""

"""
SUCCESS AND ERROR CODES FOR ATOM-STACK
==========================================
Success:
1: Success (no more information required)
2: Successfully collected data (stored in "data" key)
---
Error:
-1: Unrecoverable error (server dead or broken)
-2: Error, requires authentication to access endpoint
-11: User is already logged in
-12: Invalid username/password combination
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from ninja import NinjaAPI

from friendman.models import FriendRelationship, FriendRequestRelationship

api = NinjaAPI()


# The following API endpoints are for the sub-app "accountman"


@api.get("/api/account/info")
def account_info(request):
    try:
        if not request.user.is_authenticated:
            return {"error": "You need to be logged in to access.", "code": -2}
        user = request.user
        return {
            "success": "Collected account information.",
            "code": 11,
            "data": {
                "username": user.username,
                "email": user.email,
                "name": user.first_name + " " + user.last_name,
                "bio": user.profile.bio,
                "pfp": user.profile.profile_picture.url
            }
        }
    except:
        return {"error": "Guru Meditation.", "code": -1}


@api.post("/api/account/login")
def account_login(request, username: str, password: str):
    try:
        if request.user.is_authenticated:
            return {"error": "Request is already logged in, and must log out to log back in.", "code": -11}

        user = authenticate(username=username, password=password)
        try:
            if user is not None:
                login(request, user)
                return {"success": f"Request has been authenticated as {username}.", "code": 10}
        except:
            return {"error": "Invalid username and/or password.", "code": -12}

        return {"error": "Invalid username and/or password.", "code": -12}
    except:
        return {"error": "Guru Meditation.", "code": -1}


@api.get("/api/account/logout")
def account_logout(request):
    try:
        if not request.user.is_authenticated:
            return {"error": "You need to be logged in to access.", "code": -2}

        logout(request)
    except:
        return {"error": "Guru Meditation.", "code": -1}


# Work in Progress
@api.post("/api/account/register")
def account_register(request, first_name: str, last_name: str, username: str, email: str, password: str):
    new_user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    login(request, new_user)


# The following API endpoints are for the sub-app "friendman"


@api.get("/api/frq/{username}")
def request_friend(request, username: str):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
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


@api.get("/api/fra/{fid}")
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


@api.get("/api/frd/{fid}")
def decline_friend(request, fid: int):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
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


@api.get("/api/fd/{fid}")
def remove_friend(request, fid: int):
    if not request.user.is_authenticated:
        return {"error": "You need to be logged in to access.", "code": -2}
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
