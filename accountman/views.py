import os

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import atomtables_website.settings
from friendman.views import timestamp_to_text
from .forms import NewUserForm, EditEmailForm, EditNameForm, EditBioForm, EditPFPForm

from ninja import NinjaAPI


def register_request(request):
    x = None
    if request.user.is_authenticated:
        messages.success(request, f"No need to register: You are signed in as {request.user.username}")
        return redirect("/")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        for _, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
        print(form.errors)
        x = form.errors
    form = NewUserForm()
    return render(request=request, template_name="accountman/register.html",
                  context={"register_form": form, "messages": get_messages(request), "form_errors": x if x else None})


def login_request(request):
    x = None
    try:
        if request.GET['next'] is not None:
            redirect_url = request.GET['next']
        else:
            redirect_url = '/'
    except MultiValueDictKeyError:
        redirect_url = '/'
    if request.user.is_authenticated:
        messages.success(request, f"No need to sign in: You are signed in as {request.user.username}")
        return redirect(redirect_url)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid password. Please try again.")
        else:
            messages.error(request, "Invalid username and/or password.")
        print(form.errors)
    form = AuthenticationForm()
    return render(request=request, template_name="accountman/login.html", context={"login_form": form,
                                                                                   'login_errors': form.errors})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


def settings(request):
    print(request)
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to access this page.")
        return redirect(f"/account/login?next={request.path}")
    return render(request=request, template_name="accountman/settings.html")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accountman/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/account/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accountman/password_reset/password_reset.html",
                  context={"password_reset_form": password_reset_form})


def password_change(request):
    if not request.user.is_authenticated:
        messages.error(request, f"You need to be logged in to access this page.")
        return redirect("/account/login?next=/account/settings")
    if request.method == "POST":
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            messages.success(request, "Successfully changed password.")
            login(request, user)
            return redirect("/account/settings")
    password_change_form = PasswordChangeForm(user=request.user)
    return render(request=request, template_name="accountman/change/password_change.html",
                  context={"form": password_change_form})


def email_change(request):
    if not request.user.is_authenticated:
        messages.error(request, f"You need to be signed in to access this page.")
        return redirect("/account/login?next=/account/settings")
    if request.method == "POST":
        form = EditEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully changed Email address.")
            return redirect("/account/settings")
        messages.error(request, "Unable to change Email address. Please try again.")
    form = EditEmailForm()
    return render(request=request, template_name="accountman/change/email_change.html",
                  context={"form": form})


def name_change(request):
    if not request.user.is_authenticated:
        messages.error(request, f"You need to be signed in to access this page.")
        return redirect("/account/login?next=/account/settings")
    if request.method == "POST":
        form = EditNameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully changed Name.")
            return redirect("/account/settings")
        messages.error(request, "Unable to change Name. Please try again.")
    form = EditNameForm()
    return render(request=request, template_name="accountman/change/name_change.html",
                  context={"form": form})


def bio_change(request):
    if not request.user.is_authenticated:
        messages.error(request, f"You need to be signed in to access this page.")
        return redirect("/account/login?next=/account/settings")
    if request.method == "POST":
        form = EditBioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully changed Bio.")
            return redirect("/account/profile")
        messages.error(request, "Unable to change Bio. Please try again.")
    form = EditBioForm(initial={"bio": request.user.profile.bio})
    return render(request=request, template_name="accountman/change/bio_change.html",
                  context={"form": form})


def pfp_change(request):
    if not request.user.is_authenticated:
        messages.error(request, f"You need to be signed in to access this page.")
        return redirect("/account/login?next=/account/settings")
    if request.method == "POST":
        form = EditPFPForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if request.user.profile.profile_picture.path != atomtables_website.settings.DEF_PFP_DIR:
                os.remove(request.user.profile.profile_picture.path)
            form.save()
            messages.success(request, "Successfully changed PFP.")
            return redirect("/account/settings")
        messages.error(request, "Unable to change PFP. Please try again.")
    form = EditPFPForm()
    return render(request=request, template_name="accountman/change/pfp_change.html",
                  context={"form": form})


def user_me(request):
    context = {}
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view your friends.')
        return redirect('/account/login?next=/friend/list')
    if request.user.friend.friends is None:
        pass
    else:
        context['friends'] = []
        for x in request.user.friend.friends.all():
            if request.user == x.friend1:
                user = x.friend2
            else:
                user = x.friend1
            context['friends'] += [{
                'username': user.username,
                'pfp': user.profile.profile_picture.url,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'name': user.first_name + ' ' + user.last_name,
                'date_added': x.date_added.strftime('%B %e, %Y'),
                'last_seen': timestamp_to_text(user.profile.last_visit),
                'is_active': user.is_active,
            }]
    if request.user.friend.friend_requests is None:
        pass
    else:
        context['friend_requests'] = []
        for x in request.user.friend.friend_requests.all():
            user = x.outgoing_friend if x.incoming_friend == request.user else x.incoming_friend
            context['friend_requests'] += [{
                'username': user.username,
                'pfp': user.profile.profile_picture.url,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'name': user.first_name + ' ' + user.last_name,
                'date_added': x.date_added.strftime('%B %e, %Y'),
                'last_seen': timestamp_to_text(user.profile.last_visit),
                'outgoing': False if x.incoming_friend == request.user else True,
                'is_active': user.is_active,
            }]
    return render(request, 'friendman/userMEinfo.html', context)