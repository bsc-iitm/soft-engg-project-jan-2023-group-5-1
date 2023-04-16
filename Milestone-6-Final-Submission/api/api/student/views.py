from functools import wraps
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required , create_access_token, create_refresh_token, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request, get_jwt

import numpy as np

from ..models import Role, Ticket, User

from .. import db, jwt, model

student = Blueprint("student", __name__)





def student_required(refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if refresh:
                verify_jwt_in_request(refresh=True)
                claims = get_jwt()
                if claims["auth_level"] == "student":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)
            else:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["auth_level"] == "student":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)

        return decorator

    return wrapper





@student.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    student_role = Role.query.filter_by(name='student').first()
    student_role_id = student_role.id
    user_check = User.query.filter_by(username = username).first()
    if user_check:
        return make_response({"message": "user already exists"}, 401)
    new_student = User(username = username, email = email, role = student_role_id)
    new_student.set_password(password=password)
    db.session.add(new_student)
    db.session.commit()
    return make_response({"message": f"student {username} created"}, 201)



@student.route('/login', methods = ['POST'])
def login():
    
    
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    student_role = Role.query.filter_by(name='student').first()
    student_role_id = student_role.id
    if user.role == student_role_id:
        if user is None or not user.check_password(password):
            return make_response(jsonify({"msg": "Invalid username or password"}), 401)
        else:
            additional_claims = {"auth_level": "student", "username": user.username}
            access_token = create_access_token(identity=user, additional_claims = additional_claims)
            refresh_token = create_refresh_token(identity=user, additional_claims = additional_claims)
            resp = make_response(jsonify({'access_token': access_token}))
            resp.set_cookie('refresh_token_cookie', refresh_token, httponly=True)
            resp.set_cookie('access_token_cookie', access_token, httponly=True)
            return resp, 200
    else:
        return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)


@student.route('/logout', methods = ['POST'])
@student_required()
def logout():
    # Remove the access token cookie
    resp = make_response(jsonify({'msg': 'Successfully logged out.'}), 200)
    unset_jwt_cookies(resp)
    return resp




@student.route('/refresh', methods=['POST'])
@student_required(refresh=True)
def refresh():
    current_student_id = get_jwt_identity()
    current_student = User.query.get(current_student_id)
    additional_claims = {"auth_level": "student", "username": current_student.username}
    access_token = create_access_token(identity=current_student, additional_claims = additional_claims)
    resp = make_response(jsonify({'access_token': access_token}), 200)
    resp.set_cookie('access_token_cookie', access_token, httponly=True)
    return resp








@student.route('/change-password', methods = ['PUT'])
@student_required
def change_password():
    student_id = get_jwt_identity()
    password = request.json.get('password')
    student_user = User.query.filter_by(id = student_id).first()
    student_user.set_password(password)
    db.session.commit()
    return make_response({"message": "password changed successfully"}, 202)

