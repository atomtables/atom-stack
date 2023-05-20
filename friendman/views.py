from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


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
            for u in user.friend.friends:
                print(u)
                if u['user'] == request.user.username:
                    print(f"User {request.user.username} is friends with {u['user']}")
                    friend = 'Y'
                    break
            else:
                for u in user.friend.friend_requests:
                    print(u)
                    if u['user'] == request.user.username:
                        print(f"User {request.user.username} has a friend request to {u['user']}")
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


def redirect_to_index(request):
    return redirect('mainpage:index')
