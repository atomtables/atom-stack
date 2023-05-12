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
def add(request, username: str):
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
        user.friend.friend_requests.append(
            {
                'user': request.user.username,
                'date': int(time.time()),
                'id': sha256((request.user.username + user.username + str(int(time.time()))).encode('utf8')).hexdigest()
            }
        )
        user.save()
        return api.create_response(
            request,
            {"success": "Friend request sent"},
            status=200,
        )
