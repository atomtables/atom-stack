from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from atomtables_website import settings
from apirq import views as apirq


urlpatterns = [
    path('', include('mainpage.urls')),
    path('admin/', admin.site.urls),
    path('account/', include("accountman.urls")),
    path('chatting/', include("chatting.urls")),
    path('friend/', include("friendman.urls")),
    path("api/", apirq.api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
