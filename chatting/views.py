import os
import socketio
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=None)


def index(request):
    return render(request=request, template_name='chatting/chatpage.html')


@sio.event
def my_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)


@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])


@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)


@sio.event
def disconnect(sid):
    print('Client disconnected')
