import time
from hashlib import sha256

from django.contrib.auth.models import User
from ninja import NinjaAPI

api = NinjaAPI()


class UserAuthException(Exception):
    pass


@api.exception_handler(UserAuthException)
def user_no_auth(request, exc):
    return api.create_response(
        request,
        {"error": "You are not authorized to access this page, either due to not being logged in or "
                  "not having the correct permissions."},
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
            {"error": "User does not exist"},
            status=404,
        )
    if user is not None:
        print(user.friend.friend_requests)
        user.friend.friend_requests.append(
            {
                "user": f"{request.user.username}",
                "date": int(f"{int(time.time())}"),
                "id": f"{sha256((request.user.username + user.username + str(int(time.time()))).encode('utf8')).hexdigest()}"
            }
        )
        user.friend.save()
        return api.create_response(
            request,
            {"success": "Friend request sent"},
            status=200,
        )


@api.get("/fra/{fid}")
def add_friend(request, fid: str):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in request.user.friend.friend_requests:
        if x['id'] == fid:
            user = User.objects.get(username=x['user'])
            user.friend.friends.append(
                {
                    "user": f"{request.user.username}",
                    "date": int(f"{int(time.time())}"),
                    "id": f"{sha256((request.user.username + user.username + str(int(time.time()))).encode('utf8')).hexdigest()}"
                }
            )
            request.user.friend.friends.append(
                {
                    "user": f"{user.username}",
                    "date": int(f"{int(time.time())}"),
                    "id": f"{sha256((request.user.username + user.username + str(int(time.time()))).encode('utf8')).hexdigest()}"
                }
            )
            request.user.friend.friend_requests.remove(x)
            user.friend.save()
            request.user.friend.save()
            return api.create_response(
                request,
                {"success": "Friend added"},
                status=200,
            )
    else:
        return api.create_response(
            request,
            {"error": "Friend request not found"},
            status=404,
        )


@api.get("/frd/{fid}")
def decline_friend(request, fid: str):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in request.user.friend.friend_requests:
        if x['id'] == fid:
            request.user.friend.friend_requests.remove(x.index)
            request.user.friend.save()
            return api.create_response(
                request,
                {"success": "Friend declined"},
                status=200,
            )
    else:
        return api.create_response(
            request,
            {"error": "Friend request not found"},
            status=404,
        )


@api.get("/frd/{fid}")
def decline_friend(request, fid: str):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in request.user.friend.friend_requests:
        if x['id'] == fid:
            request.user.friend.friend_requests.remove(x.index)
            request.user.friend.save()
            return api.create_response(
                request,
                {"success": "Friend declined"},
                status=200,
            )
    else:
        return api.create_response(
            request,
            {"error": "Friend request not found"},
            status=404,
        )


@api.get("/fd/{fid}")
def remove_friend(request, fid: str):
    if not request.user.is_authenticated:
        raise UserAuthException()
    for x in range(len(request.user.friend.friends)):
        if request.user.friend.friends[x]['id'] == fid:
            user = User.objects.get(username=request.user.friend.friends[x]['user'])
            print(x)
            request.user.friend.friends.pop(x)
            request.user.friend.save()
            for y in range(len(user.friend.friends)):
                if user.friend.friends[y]['id'] == fid:
                    user.friend.friends.pop(y)
                    user.friend.save()
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
