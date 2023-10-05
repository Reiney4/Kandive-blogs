#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, User, Blogpost, User_blogposts
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class User(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO THE KANDIVE BLOGGING SITE API."
        }
        return make_response(response_message, 200)

api.add_resource(User, '/')

class Users(Resource):
    def get(self):
        users = User.query.all()
        user_list = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                
            }
            user_list.append(user_dict)
        return make_response(jsonify(user_list), 200)

api.add_resource(Users, '/users')

class UserByID(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            user_dict = {
                "id": user.id,
                "username": user.user_name,
                "email": user.email,
                "blogpost": [
                    {
                        "id": user_blogpost.blogpost.id,
                        "name": user_blogpost.blogpost.name,
                        "description": user_blogpost.blogpost.description,
                    }
                    for user_blogpost in user.blogposts
                ]
            }
            return make_response(jsonify(user_dict), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)

api.add_resource(UserByID, '/users/<int:id>')

class Blogposts(Resource):
    def get(self):
        blogposts = blogpost.query.all()
        blogpost_list = []
        for blogpost in blogposts:
            blogpost_dict = {
                "id": blogpost.id,
                "name": blogpost.name,
                "description": blogpost.description
            }
            blogpost_list.append(blogpost_dict)
        return make_response(jsonify(blogpost_list), 200)

api.add_resource(Blogposts, '/blogposts')

class User_blogposts(Resource):
    def post(self):
        data = request.get_json()

        # Validate that the required fields are present in the request
        if not all(key in data for key in ("rating", "user_id", "blogpost_id")):
            return make_response(jsonify({"errors": ["Validation error: Include all required keys"]}), 400)

        rating = data["rating"]
        blogpost_id = data["blogpost_id"]
        user_id = data["user_id"]

        # Check if the Power and Hero exist
        blogpost = blogpost.query.get(blogpost_id)
        user = User.query.get(user_id)

        if not blogpost or not user:
            return make_response(jsonify({"errors": ["Validation error: Blogpost or User doesn't exist"]}), 400)

        user_blogpost = User_blogposts(
            rating=rating,
            blogpost_id=blogpost_id,
            user_id=user_id
        )

        db.session.add(user_blogpost)
        db.session.commit()

        blogpost_data = {
            "id": blogpost.id,
            "name": blogpost.name,
            "description": blogpost.description
        }

        return make_response(jsonify(blogpost_data), 201)

api.add_resource(User_blogposts, '/user_blogposts')

@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: The requested resource does not exist.",
        404
    )
    return response

if __name__ == '__main__':
    app.run(port=5555,debug=True)
