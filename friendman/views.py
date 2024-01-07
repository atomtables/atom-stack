from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


def userpage(request, username) -> HttpResponse:
    try:
        if request.GET['error'] == 'true':
            messages.error(request, 'Unable to connect. Try again.')
        if request.GET['error'] == '403':
            messages.error(request, 'Your access is unauthorized. Please log in and try again.')
    except KeyError:
        pass
    if username == request.user.username:
        return redirect("/account/profile")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse('No such user exists', status=404)
    if user is not None:
        mutuals = []
        if request.user.is_authenticated:
            for u in user.friend.friends.all():
                if u.friend1.username == request.user.username or u.friend2.username == request.user.username:
                    friend = 'Y'
                    for f in request.user.friend.friends.all():
                        if f.friend1 != request.user:
                            fs = f.friend1
                        else:
                            fs = f.friend2

                        if fs == user:
                            continue

                        for fr in fs.friend.friends.all():
                            if fr.friend1 == user:
                                mutuals.append(
                                    {
                                        'username': fs.username,
                                        'pfp': fs.profile.profile_picture.url,
                                        'name': fs.first_name + ' ' + fs.last_name,
                                        'date_added': fr.date_added.strftime('%B %e, %Y'),
                                        'last_seen': timestamp_to_text(fs.profile.last_visit),
                                    }
                                )
                            elif fr.friend2 == user:
                                mutuals.append(
                                    {
                                        'username': fs.username,
                                        'pfp': fs.profile.profile_picture.url,
                                        'name': fs.first_name + ' ' + fs.last_name,
                                        'date_added': fr.date_added.strftime('%B %e, %Y'),
                                        'last_seen': timestamp_to_text(fs.profile.last_visit),
                                    }
                                )
                    break
            else:
                for u in user.friend.friend_requests.all():
                    if u.outgoing_friend.username == request.user.username:
                        friend = 'OR'
                        break
                    elif u.incoming_friend.username == request.user.username:
                        friend = 'IR'
                        break
                else:
                    friend = 'N'
        else:
            friend = None
        context = {
            'username': user.username,
            'pfp': user.profile.profile_picture.url,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.profile.bio,
            'friend': friend,
            'date_joined': user.date_joined.strftime('%B %e, %Y'),
            'last_seen': timestamp_to_text(user.profile.last_visit),
            'amt_friends': len(user.friend.friends.all()),
            'mutuals': mutuals,
            'is_active': user.is_active,
        }
        print(context)
        return render(request, 'friendman/userinfo.html', context)


def friend_list(request) -> HttpResponse:
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
    print(context)
    return render(request, 'friendman/friendlist.html', context)


def redirect_to_index(request):
    return redirect('/')


def friend_search(request) -> HttpResponse:
    # 1. find exact username match
    # 2. find exact name match
    # 3. find similar names
    context = {}
    try:
        query = request.GET['search']
        if request.GET['search'] == '':
            context['query_entered'] = False
            return render(request, 'friendman/friendsearch.html')
    except KeyError:
        context['query_entered'] = False
        return render(request, 'friendman/friendsearch.html')

    context['query_entered'] = True
    context['results'] = []

    try:
        if User.objects.get(username=query) is not None:
            context['results'] += {
                'username': User.objects.get(username=query).username,
                'pfp': User.objects.get(username=query).profile.profile_picture.url,
                'first_name': User.objects.get(username=query).first_name,
                'last_name': User.objects.get(username=query).last_name,
                'exact_username_match': True,
                'last_seen': timestamp_to_text(User.objects.get(username=query).profile.last_visit),
            }
    except User.DoesNotExist:
        pass
    users = list(
        (set(User.objects.filter(first_name__icontains=query, is_active=True))
         .union(User.objects.filter(last_name__icontains=query, is_active=True)))
    )
    print(list(users))


def friend_search_results(request):
    User.objects.filter(username__unaccent__lower__trigram_similar="Hélène")


def timestamp_to_text(date: datetime) -> str:
    if date.timestamp() > datetime.now().timestamp() - 60:
        return 'now'
    elif date.timestamp() > datetime.now().timestamp() - 3600:
        if int((datetime.now().timestamp() - date.timestamp()) / 60) == 1:
            return 'a minute ago'
        else:
            return '{x} minutes ago'.format(
                x=int((datetime.now().timestamp() - date.timestamp()) / 60))
    elif date.timestamp() > datetime.now().timestamp() - 89400:
        if int((datetime.now().timestamp() - date.timestamp()) / 3600) == 1:
            return 'an hour ago'
        else:
            return '{x} hours ago'.format(
                x=int((datetime.now().timestamp() - date.timestamp()) / 3600))
    else:
        if int((datetime.now().timestamp() - date.timestamp()) / 86400) == 1:
            return 'yesterday'
        else:
            return '{x} days ago'.format(
                x=int((datetime.now().timestamp() - date.timestamp()) / 86400))
