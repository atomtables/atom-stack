"""
ACCOUNTMAN API:

Error Codes:
-10: User is logged in when AnonymousUser required.
-11: Username or email already exists.
-12: Invalid username and/or password.
-13: Catastrophic Error while creating a new user.

Success Codes:
10: Collected account information.
11: Collected account information. (user is not logged in)
"""

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from ninja import Router, Schema

from atomtables_website.schemas import AuthenticationIn, SuccessData, ErrorOut, SuccessOut, UnrecoverableError, \
    NewUserIn

api = Router()


class AccountInfoNoLoginOut(SuccessData):
    success: str = "Collected account information. User is not logged in."
    code: int = 11
    info: object = {
        "is_authenticated": False
    }


class AccountInfoOut(SuccessData):
    success: str = "Collected account information."
    code: int = 10
    info: object = {
        "is_authenticated": True,
    }


class LogoutRequestOut(SuccessOut):
    success: str = "Request has been logged out."
    code: int = 1


class AuthRequiredErrorOut(ErrorOut):
    error: str = "User is not logged in."
    code: int = -2


class AuthNotRequiredErrorOut(ErrorOut):
    error: str = "User is already logged in."
    code: int = -10


class ParamEmptyErrorOut(ErrorOut):
    error: str = "Required Parameters are empty."
    code: int = -3


class InvalidUsernameOrPasswordErrorOut(ErrorOut):
    error: str = "Invalid username and/or password."
    code: int = -12


class LoginRequestOut(SuccessOut):
    success: str = "Request has been authenticated."
    code: int = 1


class InfoAlreadyExistsErrorOut(ErrorOut):
    error: str = "Username or email already exists."
    code: int = -11


class UserCreationFatalErrorOut(ErrorOut):
    error: str = "Catastrophic Error while creating a new user."
    code: int = -13

@api.get("/info", response={200: AccountInfoOut, 204: Schema, 500: UnrecoverableError})
def account_info(request):
    try:
        if not request.user.is_authenticated:
            return api.create_response(request, "", status=204)
        user = request.user
        return 200, AccountInfoOut(info={
            "is_authenticated": True,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.profile.bio,
            "pfp": user.profile.profile_picture.url
        })
    except Exception as e:
        print(e)
        return 500, UnrecoverableError()


@api.post("/signin", response={400: ParamEmptyErrorOut, 401: AuthNotRequiredErrorOut, 403: InvalidUsernameOrPasswordErrorOut, 201: LoginRequestOut, 500: UnrecoverableError})
def account_login(request, body: AuthenticationIn):
    try:
        if not body.username or not body.password:
            return 400, ParamEmptyErrorOut()

        if request.user.is_authenticated:
            return 401, AuthNotRequiredErrorOut()

        user = authenticate(username=body.username, password=body.password)
        try:
            if user is not None:
                login(request, user)
                return 201, LoginRequestOut()
        except:
            return 403, InvalidUsernameOrPasswordErrorOut()

        return 403, InvalidUsernameOrPasswordErrorOut()
    except Exception:
        return 500, UnrecoverableError()


@api.get("/signout", response={401: AuthRequiredErrorOut, 200: LogoutRequestOut, 500: UnrecoverableError})
def account_logout(request):
    try:
        if not request.user.is_authenticated:
            return 401, AuthRequiredErrorOut()

        logout(request)
        return 200, LogoutRequestOut()
    except:
        return 500, UnrecoverableError()


@api.post("/register")
def account_register(request, body: NewUserIn):
    username, password, email, first_name, last_name = body.username, body.password, body.email, body.firstName, body.lastName
    try:
        if not username or not password or not email or not first_name or not last_name:
            return 400, ParamEmptyErrorOut()

        if request.user.is_authenticated:
            return 401, AuthNotRequiredErrorOut()

        if (User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()):
            return 400, InfoAlreadyExistsErrorOut()

        try:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        except:
            return 500, UserCreationFatalErrorOut()

        login(request, new_user)
        return 201, LoginRequestOut()
    except Exception:
        return {"error": "Guru Meditation.", "code": -1}
