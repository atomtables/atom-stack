"""
ATOM-STACK API:
Keeps the frontend logically separate from the backend, allowing for more
expansive frontend development, as well as a self-hosted backend that doesn't
rely on Firebase, and can easily be replicated on "dev" and "prod"
"""
from typing import Any, Optional

from django.http import HttpRequest, HttpResponse

"""
Success Codes:
1:     Success with void (no return)
2:     Success with data (data key contains important information)
10-19: Account-MAN specific success

Error Codes:
-1:     Fatal uncaught error ("Guru Meditation")
-2:     Authentication required
-3:     Empty arguments
-4:     API Key Invalid
-10-19: Account-MAN specific error
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from ninja.security import APIKeyHeader, HttpBearer

from atomtables_website import settings

class InvalidToken(Exception):
    pass
class Authorization(HttpBearer):
    def authenticate(self, request, token):
        if token == settings.SECRET_KEY:
            return token

        raise InvalidToken()

class NAPI(NinjaAPI):
    def create_response(self, *a, **kw) -> HttpResponse:
        response = super().create_response(*a, **kw)
        response["Content-Type"] = "application/json"
        response["Access-Control-Allow-Origin"] = "*"
        return response

api = NAPI(auth=Authorization())
@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    return api.create_response(request, {"error": "API Key Invalid.", "code": -4}, status=401)

api.add_router("/account", "accountman.views.api")
api.add_router("/friend", "friendman.views.api")

urlpatterns = [
    path('', api.urls),
    path('admin', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
