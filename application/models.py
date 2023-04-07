from .database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime



class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    profile_pic = db.Column(db.Text)
    following = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    home_town = db.Column(db.String)
    # login_time = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary = 'role_users', backref = db.backref('users', lazy = 'dynamic') )
    posting = db.relationship("Posts", backref = "User", cascade="all, delete-orphan")
    user_commenting = db.relationship("Comment",backref = "User", cascade="all, delete-orphan")
    

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))

class Posts(db.Model):
    __tablename__ = "Posts"
    post_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    post_name = db.Column(db.String, nullable = False)
    post_caption = db.Column(db.String, nullable = False)
    post_image = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))
    date = db.Column(db.String)
    time = db.Column(db.String)
    post_like = db.Column(db.Integer)
    commenting = db.relationship("Comment",backref = "Posts", cascade="all, delete-orphan")

class Comment(db.Model):
    __tablename__ = "Comments"
    comment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    comment = db.Column(db.Text, nullable = False)
    comment_like = db.Column(db.Integer)
    post_id = db.Column(db.Integer, db.ForeignKey(Posts.post_id, ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))

class Follow(db.Model):
    __tablename__ = "Follow"
    user_1 = db.Column(db.Integer, db.ForeignKey("User.id", ondelete='CASCADE'), nullable = False)
    user_2 = db.Column(db.Integer, db.ForeignKey("User.id", ondelete='CASCADE'), nullable = False)
    follow_id = db.Column(db.Integer, primary_key = True, autoincrement = True)


role_users = db.Table('role_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('User.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)







