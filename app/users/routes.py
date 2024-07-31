from flask import render_template, redirect, url_for, request, session, flash

from app.extensions import db
from app.users import bp
from app.models.User import User
from app.models.JoinTables import UsersRooms


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user is None:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                session['username'] = username
                return redirect(url_for('chat.index'))
            else:
                flash('Username already exists!')
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('chat.index'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('users.login'))
