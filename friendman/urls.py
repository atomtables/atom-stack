from django.urls import path

from . import views

urlpatterns = [
    path("user/<str:username>/", views.userpage, name="userpage"),
    path("user/", views.redirect_to_index, name="redirect_to_index"),
    path("", views.redirect_to_index, name="redirect_to_index"),
]
