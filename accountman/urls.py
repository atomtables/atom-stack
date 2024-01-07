from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("settings/", views.settings, name="settings"),
    path("profile/", views.user_me, name="user_me"),
    path("settings/email-change", views.email_change, name="email-change"),
    path("settings/name-change", views.name_change, name="name-change"),
    path("settings/bio-change", views.bio_change, name="bio-change"),
    path("settings/pfp-change", views.pfp_change, name="pfp-change"),
    path("settings/password-change", views.password_change, name="password-change"),
    path(
        "password_reset/",
        views.password_reset_request,
        name="password_reset"
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accountman/password_reset/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accountman/password_reset/password_reset_confirm.html"),
         name='password_reset_confirm'
         ),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accountman/password_reset/password_reset_complete.html'),
         name='password_reset_complete'
         ),
]
