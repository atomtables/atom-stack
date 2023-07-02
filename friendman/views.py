from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime


def userpage(request, username):
    try:
        if request.GET['error'] == 'true':
            messages.error(request, 'Unable to connect. Try again.')
        if request.GET['error'] == '403':
            messages.error(request, 'Your access is unauthorized. Please log in and try again.')
    except KeyError:
        pass
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('No such user exists', status=404)
    if user is not None:
        print(f"User {user} found")
        if user.username == request.user.username:
            return HttpResponse('sneaky user this is you lmao', status=400)
        if user.is_authenticated:
            for u in user.friend.friends.all():
                print(u)
                if u.friend1.username == request.user.username or u.friend2.username == request.user.username:
                    print(f"User {request.user.username} is friends with {user.username}")
                    friend = 'Y'
                    break
            else:
                for u in user.friend.friend_requests.all():
                    print(u)
                    if u.outgoing_friend.username == request.user.username:
                        print(f"User {request.user.username} sent a friend request to {user.username}")
                        friend = 'R'
                        break
                    elif u.incoming_friend.username == request.user.username:
                        print(f"User {request.user.username} has a friend request from {user.username}")
                        friend = 'R'
                        break
                else:
                    print(f"User {request.user.username} is not friends with {user.username}")
                    friend = 'N'
        else:
            friend = 'S'
        context = {
            'username': user.username,
            'pfp': user.profile.profile_picture.url,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.profile.bio,
            'friend': friend,
            'date_joined': user.date_joined.strftime('%B %e, %Y'),
            'last_login': user.last_login.strftime('%B %e, %Y') if user.last_login is not None else 'Never',
        }
        return render(request, 'friendman/userinfo.html', context)


def friend_list(request):
    context = {}
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to view your friends.')
        return redirect('/account/login?next=/friend/list')
    if request.user.friend.friends is None:
        pass
    else:
        for x in request.user.friend.friends.all():
            if request.user == x.friend1:
                user = x.friend2
            else:
                user = x.friend1
            last_seen = user.profile.last_visit
            if last_seen.timestamp() > datetime.now().timestamp() - 300:
                status = 'Online'
            elif last_seen.timestamp() > datetime.now().timestamp() - 89400:
                if int((datetime.now().timestamp() - last_seen.timestamp()) / 3600) == 1:
                    status = 'Last seen an hour ago'
                else:
                    status = 'Last seen {x} hours ago'.format(x=int((datetime.now().timestamp() - last_seen.timestamp()) / 3600))
            else:
                if int((datetime.now().timestamp() - last_seen.timestamp()) / 86400) == 1:
                    status = 'Last seen yesterday'
                else:
                    status = 'Last seen {x} days ago'.format(x=int((datetime.now().timestamp() - last_seen.timestamp()) / 86400))
            context['friends'] = context.get('friends', []) + [{
                'user': user.username,
                'pfp': user.profile.profile_picture.url,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_added': x.date_added.strftime("%d/%m/%Y"),
                'status': status,
            }]
    print(context)
    return render(request, 'friendman/friendlist.html', context)


def redirect_to_index(request):
    return redirect('mainpage:index')
