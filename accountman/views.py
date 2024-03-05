"""
ACCOUNTMAN API:

Error Codes:
-10: User is logged in when AnonymousUser required.
-11: Username or email already exists.
-12: Invalid username and/or password.

Success Codes:
10: Collected account information.
11: Collected account information. (user is not logged in)
"""

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from ninja import Router, Schema

api = Router()

class SignInSchema(Schema):
    username: str
    password: str

@api.get("/info")
def account_info(request):
    print(request.COOKIES, request.user.is_authenticated, request.user)
    try:
        if not request.user.is_authenticated:
            return api.create_response(request, {
                "success": "Collected account information. User is not logged in.",
                "code": 11,
                "info": {
                    "is_authenticated": False,
                    "username": None,
                    "email": None,
                    "first_name": None,
                    "last_name": None,
                    "bio": None,
                    "pfp": None
                }
            }, status=200)
        user = request.user
        return api.create_response(request, {
            "success": "Collected account information.",
            "code": 10,
            "info": {
                "is_authenticated": True,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "bio": user.profile.bio,
                "pfp": user.profile.profile_picture.url
            }
        }, status=200)
    except Exception as e:
        return {"error": f"Guru Meditation: {e}", "code": -1}

@api.get("/isauth")
def account_is_authenticated(request):
    try:
        if not request.user.is_authenticated:
            return {"success": "User is not logged in.", "code": 11}
        return {"success": "User is logged in.", "code": 10}
    except:
        return {"error": "Guru Meditation.", "code": -1}

@api.post("/signin")
def account_login(request, body: SignInSchema):
    try:
        if not body.username or not body.password:
            return {"error": "Required Parameters are empty", "code": -3}

        if request.user.is_authenticated:
            return {"error": "Request is already logged in.", "code": -10}

        user = authenticate(username=body.username, password=body.password)
        try:
            if user is not None:
                login(request, user)
                return {"success": f"Request has been authenticated as {body.username}.", "code": 1}
        except:
            return {"error": "Invalid username and/or password.", "code": -12}

        return {"error": "Invalid username and/or password.", "code": -12}
    except Exception as e:
        print(f"Exception: {e}")
        return {"error": "Guru Meditation.", "code": -1}


@api.get("/signout")
def account_logout(request):
    try:
        if not request.user.is_authenticated:
            return {"error": "You need to be logged in to access.", "code": -2}

        logout(request)
        return {"success": "Request has been logged out.", "code": 1}
    except:
        return {"error": "Guru Meditation.", "code": -1}


@api.post("/register")
def account_register(request, first_name: str, last_name: str, username: str, email: str, password: str):
    try:
        if not username or not password or not email or not first_name or not last_name:
            return {"error": "Required Parameters are empty", "code": -3}

        if request.user.is_authenticated:
            return {"error": "Request is already logged in.", "code": -10}

        if (User.objects.exclude(pk=request.pk).filter(username=username).exists()
                or User.objects.exclude(pk=request.pk).filter(email=email).exists()):
            return {"error": "Username or email already exists.", "code": -11}

        try:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        except:
            return {"error": "Unable to make user.", "code": -1}

        login(request, new_user)
        return {"success": f"Request has been authenticated as {username}.", "code": 1}
    except:
        return {"error": "Guru Meditation.", "code": -1}
