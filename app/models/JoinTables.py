from app import db


class UsersRooms(db.Model):
    __tablename__ = 'users_rooms'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)