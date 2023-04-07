from flask import Flask, request, redirect, flash
from flask import render_template, request
from flask import current_app as app
from .models import User, Posts, Follow
from .database import db
from flask_security import roles_required
from flask_security import login_required, Security
from flask_login import current_user
from main import user_datastore, app
from flask_security import login_user, logout_user, login_required, current_user
from flask_security.utils import hash_password
from flask_security import login_required, LoginForm
from datetime import datetime


def check_password(pwd):
    if len(pwd) < 5:
        return False
    
    return True


@app.route("/")
def general():
    return render_template("general.html")



@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if check_password(password) == True:
            
            if password != c_password:
                return render_template('pass_error.html')
            user_datastore.create_user(
                username = username,
                password = hash_password(password),
                email = email,
                first_name = first_name, last_name = last_name
            , profile_pic = "default.jpg", followers = 0, following = 0
            )
            
            db.session.commit()

            login_user(current_user)
            
            return redirect("/home_page")
        else:
            return render_template("register.html", check = False)
    return render_template("register.html", check = True)





@app.route("/home_page", methods = ["GET"])
@login_required
def home():
    
    user_name = current_user.username
    user = User.query.filter_by(username = user_name).first()
    user.login_time = datetime.utcnow()
    db.session.commit()
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"
    sql_fole = Follow.query.filter_by(user_1 = user_name).all()
    
            
    followees = []
    for i in sql_fole:
        
        sql_user = User.query.filter_by(username = i.user_2).first()
        
        sql_user_posts = Posts.query.filter_by(user_id = sql_user.id).all()
        
        followee_posts = []
        for j in sql_user_posts:
            
            sql_post = Posts.query.filter_by(post_id = j.post_id).first()
            followee_posts.append((sql_post.post_name, sql_post.post_caption, sql_post.post_image, sql_user.username, sql_user.profile_pic, sql_post.post_id,
                    sql_post.post_like, sql_post.date, sql_post.time))
            
        followees.append(followee_posts)
    
    return render_template("home.html", user = user, user_name = user_name, image = user.profile_pic
    ,followees = followees, home_town = user.home_town)



