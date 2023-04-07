from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from .models import User, Posts, Follow, Comment
from .database import db
from flask_login import current_user

@app.route("/follow/<user_2>", methods = ["GET", "POST"])
def follow(user_2):
    user_1 = current_user.username
    sql = Follow(user_1 = user_1, user_2 = user_2)
    db.session.add(sql)
    db.session.commit()
    sql1 = User.query.filter_by(username = user_1).first()
    
    sql1.following += 1
    sql2 = User.query.filter_by(username = user_2).first()
    sql2.followers += 1
    db.session.commit()
    
    return redirect("/profile/" + user_2)

@app.route("/unfollow/<user_2>", methods = ["GET", "POST"])
def unfollow(user_2):
    user_1 = current_user.username
    sql = db.session.query(Follow).filter((Follow.user_1 == user_1) & (Follow.user_2 == user_2)).first()
    db.session.delete(sql)
    sql1 = User.query.filter_by(username = user_1).first()
    sql1.following -= 1
    sql2 = User.query.filter_by(username = user_2).first()
    sql2.followers -= 1
    db.session.commit()
    db.session.commit()
    
    return redirect("/profile/" + user_2)

@app.route("/followers/<user_2>")
def display_followers(user_2):
    user_1 = current_user.username
    sql = Follow.query.filter_by(user_2 = user_2).all()
    sql2 = User.query.filter_by(username = user_1).first()
    
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"
    followers = []
    for i in sql:
        sql1 = User.query.filter_by(username = i.user_1).first()
        followers.append((i.user_1, sql1.profile_pic))

    return render_template("followers.html", followers = followers, user_name = user_1, image = sql2.profile_pic)

@app.route("/followee/<user_2>")
def display_followee(user_2):
    user_1 = current_user.username
    sql = Follow.query.filter_by(user_1 = user_2).all()
    sql2 = User.query.filter_by(username = user_1).first()
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"
    
    
    followees = []
    for i in sql:
        sql1 = User.query.filter_by(username = i.user_2).first()
        followees.append((i.user_2, sql1.profile_pic))
    return render_template("followee.html", followees = followees, user_name = user_1, image = sql2.profile_pic)