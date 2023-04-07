from flask_restful import Resource, Api, fields, marshal_with, reqparse
from werkzeug .exceptions import HTTPException
from flask import make_response
from .database import db
from .models import User, Posts
import json
from datetime import datetime

post_fields_1 = {
   "post_id" : fields.Integer
}
create_post_parser = reqparse.RequestParser() 
create_post_parser.add_argument('post_name')
create_post_parser.add_argument('caption')
create_post_parser.add_argument('image')

update_post_parser = reqparse.RequestParser() 
update_post_parser.add_argument('post_name')
update_post_parser.add_argument('post_caption')
update_post_parser.add_argument('post_image')



post_fields_2 = {
    "post_id" : fields.Integer,
    "post_name" : fields.String,
    "post_caption" : fields.String,
    "post_image" : fields.String
}

post_fields_3 = post_fields_2 = {
    "post_id" : fields.Integer,
    "post_name" : fields.String,
}

class NotFoundError(HTTPException):
    def __init__(self,status_code):
        self.response = make_response('',status_code)
class BuisnessValidationError(HTTPException):
    def __init__(self,status_code,error_code,error_message):
        message = {'error_code':error_code,'error_message':error_message}
        self.response = make_response(json.dumps(message),status_code)

class PostAPI(Resource):
    @marshal_with(post_fields_1)
    def get(self, user_name):
        sql = User.query.filter_by(user_name = user_name).first()
        if sql:
            sql1 = Posts.query.filter_by(user_id = sql.id).all()
            return sql1
        else:
            raise BuisnessValidationError(status_code=400, error_code ='USER002',error_message = 'User Name is required')
    @marshal_with(post_fields_2)
    def post(self, user_name):
        sql1 = User.query.filter_by(username = user_name).first()
        args = create_post_parser.parse_args()
        post_name = args.get("post_name", None)
        caption = args.get("caption", None)
        image = args.get("image", None)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt = dt_string.split(" ")
        date, time = dt[0], dt[1]
        if not post_name:
            raise BuisnessValidationError(status_code=400, error_code ='POST001',error_message = 'Post Name is required')
        if not caption:
            raise BuisnessValidationError(status_code=400, error_code ='POST002',error_message = 'Post description is required')
        sql = Posts(post_name = post_name, post_caption = caption, post_image = image, user_id = sql1.user_id, date = date, time = time
        , post_like = 0)
        db.session.add(sql)
        db.session.commit()
        return sql

    @marshal_with(post_fields_3)  
    def put(self, post_id):
        
        sql2 = Posts.query.filter_by(post_id = post_id).first()
        if sql2:
            sql = Posts.query.filter_by(post_id = post_id).first()
            args = update_post_parser.parse_args()
            post_name = args.get("post_name", None)
            caption = args.get("post_caption", None)
            image = args.get("post_image", None)
            if not post_name:
                raise BuisnessValidationError(status_code=400, error_code ='POST001',error_message = 'Post Name is required')
            if not caption:
                raise BuisnessValidationError(status_code=400, error_code ='POST002',error_message = 'Post description is required')

            sql.post_name = post_name
            sql.post_caption = caption
            if image is not None:
                sql.post_image = image
            else:
                sql.post_image = sql.post_image
            db.session.commit()
            return sql
        return NotFoundError(status_code = 404)


    def delete(self, post_id):
        sql = Posts.query.filter_by(post_id = post_id).first()
        if sql:
            db.session.delete(sql)
            db.session.commit()
            return "Successfully Deleted", 200
        return NotFoundError(status_code = 404)
        
