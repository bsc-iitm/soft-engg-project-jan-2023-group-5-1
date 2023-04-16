from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required , create_access_token, create_refresh_token, get_jwt_identity, current_user, unset_jwt_cookies

from .models import Role, User

from . import db






views = Blueprint("views", __name__)

@views.route('/', methods = ['GET', 'POST'])
def home():
    return make_response({"message": "AbulAman"}, 200)










# @views.route('/add-roles', methods = ['GET'])
# def add_roles():
#     student_role = Role(name='student', description='Student')
#     staff_role = Role(name='staff', description='Staff member')
#     admin_role = Role(name='admin', description='Administrator')

#     db.session.add_all([student_role, staff_role, admin_role])
#     db.session.commit()

#     return make_response({'message': 'roles added...'}, 201)