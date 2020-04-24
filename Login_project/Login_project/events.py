from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from . import db
from .models import User, Connection
from flask_socketio import emit, join_room, leave_room
from . import socketio
from datetime import datetime, timedelta

events = Blueprint('events', __name__)

@socketio.on('connect', namespace='/connectStatus')
def logeventComingUser():
    #update number of connection as new activity detected (refresh page or open new tab or visit new page)
    now = datetime.now()
    if current_user.is_authenticated:
        user = User.query.filter_by(name=current_user.name).first() # if this returns a user, then the email already exists in database
        if user:
            user.lastActivity = now
            if user.numberConnection == None or (now > (user.lastActivity  + timedelta(hours=2))):
                user.numberConnection = 1
            else:
                user.numberConnection += 1
            db.session.commit()
            print(current_user.name + ' came on boardGame and is tracked')
        else:
            print('can not retrieve connected user in DB while connecting, strange...')
    else:
        print('anonymous came on boardGame')

@socketio.on('disconnect', namespace='/connectStatus')
def test_disconnect():
    now = datetime.now()
    if current_user.is_authenticated:
        user = User.query.filter_by(name=current_user.name).first() # if this returns a user, then the email already exists in database
        if user:
            user.lastDisconnect = now
            user.numberConnection -= 1
            db.session.commit()
            print(current_user.name + ' left boardGame and is tracked')
        else:
            print('can not retrieve connected user in DB while disconnecting, strange...')
    else:
        print('anonymous left boardGame')

@socketio.on('connect',namespace='/test')
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