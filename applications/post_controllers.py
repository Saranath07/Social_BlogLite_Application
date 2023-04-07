from flask import Flask, render_template, request, redirect, url_for, make_response, session
from flask import current_app as app
from .models import User, Posts
from .database import db
from datetime import datetime
from flask_login import current_user
from flask_security import login_required


app.config['UPLOAD_FOLDER'] = "static\images"


@app.route("/add_post", methods = ["GET", "POST"])
@login_required
def add_post():
    user_name = current_user.username
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt = dt_string.split(" ")
    date, time = dt[0], dt[1]
    sql2 = User.query.filter_by(username = user_name).first()
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"
    if sql2:
        if request.method == "GET":
            return render_template('add_post.html', user_name = user_name, image = sql2.profile_pic)
            
        elif request.method == "POST":
            
            name = request.form['name']
            caption = request.form['caption']
            image = request.files['imageFile']
            
            user = User.query.filter_by(username = user_name).first()
            
            if image.filename != "":
                file_path = "static/" + image.filename
                image.save(file_path)
                
                
                sql = Posts(post_name = name, post_caption = caption, post_image = image.filename, post_like = 0
                    ,date = date, time = time, user_id = user.id)
                
                db.session.add(sql)
                
                db.session.commit()
                
                
                return redirect("/profile/" + user_name)
            else:
                sql = Posts(post_name = name, post_caption = caption, user_id = user.id, post_image = "NA"
                ,date = date, time = time,)
                
                db.session.add(sql)
                db.session.commit()
                
                
               
                return redirect("/profile/" + user_name)
    return "Error"

@app.route("/edit_post/<post_id>", methods = ["GET", "POST"])
@login_required
def edit_post(post_id):
    user_name = current_user.username
    sql2 = Posts.query.filter_by(post_id = post_id).first()
    sql1 = User.query.filter_by(id = current_user.id).first()
    # return sql2.post_image
    
    user_info = request.args.get('username')
    if user_info:
        users = User.query.filter(User.username.contains(user_info)).all()
        if users:
            return render_template("search.html", users = users) 
        return "User does not exist"

    if request.method == "GET":
        return render_template('edit_post.html' ,post_id = post_id, 
        Name = sql2.post_name, Caption = sql2.post_caption, Image = sql2.post_image)
        
    elif request.method == "POST":
        
        name = request.form['name']
        
        caption = request.form['caption']
        image = request.files['imageFile']
        

        if name != "":
                sql2.post_name = name
        
        if caption != "":
            sql2.post_caption = caption
        
        if image.filename != "":
            file_path = "static/" + image.filename
            image.save(file_path)
            
            
            
            sql2.post_image = image.filename
        sql2.post_like = 0
        
        db.session.commit()
            
        return redirect("/profile/" + sql1.username)
           
                
                
                
                
    return "Error"


@app.route("/delete_post/<post_id>", methods = ["GET", "POST", "DELETE"])
@login_required
def delete_post(post_id):
    user_name = current_user.username
    if request.method == "POST":
        post = Posts.query.filter_by(post_id = post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect("/profile/" + user_name)
    return render_template("post_delete_confo.html", post_id = post_id)

