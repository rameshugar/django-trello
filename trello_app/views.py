from django.shortcuts import render, redirect
from django.contrib.auth import login, logout as auth_logout
from django.conf import settings

from trello_app.models import UserProfile, User

from trello import TrelloApi


def connect_to_trello(token):
    trello = TrelloApi(settings.TRELLO_API_KEY)
    trello.set_token(token)
    return trello

def home(request):
    context_dict = {}
    if request.user.is_authenticated():
        trello = connect_to_trello(request.user.userprofile.user_token)
        context_dict['members'] = trello.boards.get_member('3KQ4HLl0')
    return render(request, 'home.html', context_dict)

def auth(request):
    if request.GET.get('token'):
        user_token = request.GET.get('token')
        trello = connect_to_trello(user_token)
        member = trello.tokens.get_member(user_token)
        user, created = User.objects.get_or_create(
            username=member.get('username'),
            email='test@test.com',
            first_name=member.get('fullName'))
        user.userprofile.user_token = user_token
        user.userprofile.save()
        login(request, user)
    return redirect('home')

def logout(request):
    auth_logout(request)
    return redirect('home')