from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from atomtables_website import settings
from atomtables_website import api as api
from friendman import api as friend_api


urlpatterns = [
    path('', include('mainpage.urls')),
    path('', api.api.urls),
    path('admin/', admin.site.urls),
    path('account/', include("accountman.urls")),
    path('chatting/', include("chatting.urls")),
    path('friend/', include("friendman.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
