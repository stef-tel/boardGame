from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from . import db
from .models import User, Connection
from flask_socketio import emit, join_room, leave_room
from . import socketio
from datetime import datetime

events = Blueprint('events', __name__)

#@socketio.on('connect', namespace='/test')
@socketio.on('connect')
def login_connect():
    if current_user.is_authenticated:
        #update connection history
        now = datetime.now()
        newConnection = Connection(player_id = current_user.id,
                                    dateTime = now,
                                    status='open')
        db.session.add(newConnection)
        #db.session.flush() 
        db.session.commit()
        emit('my response', {'data': 'Connected'})
    else:
        return False
    print('client connected')

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


@socketio.on('joined', namespace='/globalChat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = 'general_room'
    join_room(room)
    emit('status', {'msg': current_user.name + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/globalChat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = 'general_room'
    #emit('message', {'msg': current_user.name + ':' + message['msg']}, room=room)
    emit('message', {'sender': current_user.name, 'msg' : message['msg'] }, room=room)


@socketio.on('left', namespace='/globalChat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = 'general_room'
    leave_room(room)
    emit('status', {'msg': current_user.name + ' has left the room.'}, room=room)