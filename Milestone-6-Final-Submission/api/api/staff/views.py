from functools import wraps
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required , create_access_token, create_refresh_token, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request, get_jwt

from ..models import Role, User, Faq, Ticket

from .. import db, jwt

staff = Blueprint("staff", __name__)




def staff_required(refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if refresh:
                verify_jwt_in_request(refresh=True)
                claims = get_jwt()
                if claims["auth_level"] == "staff":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)
            else:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["auth_level"] == "staff":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)

        return decorator

    return wrapper




@staff.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    staff_role = Role.query.filter_by(name='staff').first()
    staff_role_id = staff_role.id
    user_check = User.query.filter_by(username = username).first()
    if user_check:
        return make_response({"message": "user already exists"}, 401)
    elif username is None or password is None or email is None:
        return make_response({"message": "bad request"}, 400)
    new_staff = User(username = username, email = email, role = staff_role_id)
    new_staff.set_password(password=password)
    db.session.add(new_staff)
    db.session.commit()
    return make_response({"message": f"Staff {username} created"}, 201)







@staff.route('/login', methods = ['POST'])
def login():
    
    
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    staff_role = Role.query.filter_by(name='staff').first()
    staff_role_id = staff_role.id
    if user.role == staff_role_id:
        if user is None or not user.check_password(password):
            return make_response(jsonify({"msg": "Invalid username or password"}), 401)
        else:
            additional_claims = {"auth_level": "staff", "username": user.username}
            access_token = create_access_token(identity=user, additional_claims = additional_claims)
            refresh_token = create_refresh_token(identity=user, additional_claims = additional_claims)
            resp = make_response(jsonify({'access_token': access_token}))
            resp.set_cookie('refresh_token_cookie', refresh_token, httponly=True)
            resp.set_cookie('access_token_cookie', access_token, httponly=True)
            return resp, 200
    else:
        return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)


@staff.route('/logout', methods = ['POST'])
@staff_required()
def logout():
    # Remove the access token cookie
    resp = make_response(jsonify({'msg': 'Successfully logged out.'}), 200)
    unset_jwt_cookies(resp)
    return resp



@staff.route('/refresh', methods=['POST'])
@staff_required(refresh=True)
def refresh():
    current_staff_id = get_jwt_identity()
    current_staff = User.query.get(current_staff_id)
    additional_claims = {"auth_level": "staff", "username": current_staff.username}
    access_token = create_access_token(identity=current_staff, additional_claims = additional_claims)
    resp = make_response(jsonify({'access_token': access_token}), 200)
    resp.set_cookie('access_token_cookie', access_token, httponly=True)
    return resp

@staff.route('/change-password', methods = ['PUT'])
@staff_required
def change_password():
    staff_id = get_jwt_identity()
    password = request.json.get('password')
    staff_user = User.query.filter_by(id = staff_id).first()
    staff_user.set_password(password)
    db.session.commit()
    return make_response({"message": "password changed successfully"}, 202)


