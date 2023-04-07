from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from .models import User, Posts, Comment, Follow
from .database import db
from flask_login import current_user
from flask_security import login_required

@app.route("/profile/<user_name>")
def profile(user_name):
    sql = User.query.filter_by(username = user_name).first()
    
    if sql:
        user_id = sql.id
        total_posts = Posts.query.filter_by(user_id = user_id).all()
        total_following = Follow.query.filter_by(user_2 = user_name).all()
        total_followers = Follow.query.filter_by(user_1 = user_name).all()
        user_info = request.args.get('username')
        if user_info:
            users = User.query.filter(User.username.contains(user_info)).all()
            if users:
                return render_template("search.html", users = users) 
            return "User does not exist"
        following = db.session.query(Follow).filter((Follow.user_1 == current_user.username) & (Follow.user_2 == user_name)).first()
        result = False
        if following:
            result = True
        # return render_template("dummy.html", sql = total_posts)
        uposts = Posts.query.filter_by(user_id = user_id).all()
        total_posts = 0
        posts = []
        for post in uposts:
            total_posts += 1
            user = User.query.filter_by(id = post.user_id).first()
            comments = Comment.query.filter_by(post_id = post.post_id).all()
            post_comments = []
            for comment in comments:
                sql1 = User.query.filter_by(id = comment.user_id).first()
                post_comments.append((comment.comment, comment.comment_like, sql1.profile_pic, sql1.username, comment.comment_id))
            posts.append((post.post_name, post.post_caption, post.post_image, post.post_id
            , user.username, post.date, post.time, post_comments, post.post_like))
        
        
                
        
        return render_template("profile.html", posts = posts, 
                    user_name = sql.username, f_name = sql.first_name, l_name = sql.last_name, image = sql.profile_pic,
                    result = result, total_posts = total_posts, foll1 = len(total_followers), foll2 = len(total_following))
    return f"No user Found"
@app.route("/settings", methods = ["GET", "POST"])
@login_required
def settings():
    
    user_name = current_user.username
    sql2 = User.query.filter_by(username = user_name).first()
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"
    if sql2:
        if request.method == "POST":
            profile_pic = request.files['profile_pic']
            
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            home_town = request.form['home_town']
            
            
            if profile_pic.filename != "":
                file_path = "static/" + profile_pic.filename
                profile_pic.save(file_path)
                
                
                sql2.profile_pic = profile_pic.filename
                
            
            
            
            if first_name != "":
                sql2.first_name = first_name
            if last_name != "":
                sql2.last_name = last_name
            if home_town != "":
                sql2.home_town = home_town
            db.session.commit()

        

        return render_template("settings.html")

    return "Error"

@app.route("/comment/<user_name>/<post_id>", methods = ["GET", "POST"])
def post_comment(user_name, post_id):
    sql = Posts.query.filter_by(post_id = post_id).first()
    sql1 = User.query.filter_by(username = user_name).first()
    sql3 = User.query.filter_by(id = sql.user_id).first()
    if request.method == "POST":
        
        comment = request.form['comment']
        add_comment = Comment(comment = comment, comment_like = 0, post_id = post_id, user_id = sql1.id)
        db.session.add(add_comment)
        db.session.commit()
        
        return redirect("/profile/" + sql3.username)
    return render_template("add_comment.html", post_id = post_id, user_name = user_name)

@app.route("/like/<post_id>")
def like(post_id):
    sql = Posts.query.filter_by(post_id = post_id).first()
    sql1 = User.query.filter_by(id = sql.user_id).first()
    sql.post_like += 1
    db.session.commit()
    return redirect("/profile/" + sql1.username)

@app.route("/comment_like/<comment_id>")
def comment_like(comment_id):
    sql = Comment.query.filter_by(comment_id = comment_id).first()
    sql2 = Posts.query.filter_by(post_id = sql.post_id).first()
    sql1 = User.query.filter_by(id = sql2.user_id).first()
    sql.comment_like += 1
    db.session.commit()
    return redirect("/profile/" + sql1.username)

    
    
  



@app.route("/delete_account", methods = ["GET", "POST"])
@login_required
def delete_account():
    user_name = current_user.username
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"
    if request.method == "GET":
        return render_template("user_delete_confo.html", user_name = user_name)
    if request.method == "POST":
        user = User.query.filter_by(username = user_name).first()
        
        db.session.delete(user)
        follow = db.session.query(Follow).filter((Follow.user_1 == current_user.username) | (Follow.user_2 == current_user.username)).all()
        for i in follow:
            db.session.delete(i)
        db.session.commit()
    return redirect("/")