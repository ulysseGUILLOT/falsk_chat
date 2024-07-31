from flask import render_template, redirect, url_for, request, session, flash
from flask_socketio import join_room, send, leave_room

from app.extensions import db
from app.extensions import socketio
from app.chat import bp
from app.models.Room import Room
from app.models.User import User
from app.models.Message import Message
from app.models.JoinTables import UsersRooms


@bp.route('/')
def index():
    if not session.get('username'):
        return redirect(url_for('users.login'))

    username = session['username']
    user = User.query.filter_by(username=username).first()
    rooms = user.rooms if user else []
    users = User.query.all()
    users.remove(user)
    return render_template('index.html', rooms=rooms, username=username, users=users)


@bp.route('/newroom', methods=["GET", "POST"])
def create_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        room = Room(name=room_name)
        db.session.add(room)

        selected_user_id = request.form.getlist('users')
        users = []
        for user_id in selected_user_id:
            user = User.query.filter_by(id=user_id).first()
            if user:
                users.append(user)

        connected_username = session['username']
        connected_user = User.query.filter_by(username=connected_username).first()
        if connected_user:
            users.append(connected_user)

        for user in users:
            user.rooms.append(room)

        db.session.commit()

    return redirect(url_for('chat.index'))


@bp.route('/chat/<int:room_id>', methods=['GET', 'POST'])
def chat(room_id):
    if not session.get('username'):
        return redirect(url_for('users.login'))

    username = session['username']
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.timestamp.asc()).all()

    return render_template('chat.html', room_id=room_id, username=username, messages=messages)


@socketio.on('join')
def handle_join(data):
    username = data['username']
    room_id = data['room_id']
    join_room(room_id)
    send(f'{username} has joined the room.', room=room_id)


@socketio.on('message')
def handle_message(data):
    username = data['username']
    content = data['msg']
    room_id = data['room_id']
    send(f'{username} : {content}', room=room_id)

    user = User.query.filter_by(username=username).first()

    if user:
        new_message = Message(content=content, room_id=room_id, user_id=user.id)
        db.session.add(new_message)
        db.session.commit()


@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room_id = data['room_id']
    leave_room(room_id)
    send(f'{username} has left the room.', room=room_id)
