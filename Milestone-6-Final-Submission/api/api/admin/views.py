from functools import wraps
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required , create_access_token, create_refresh_token, get_jwt_identity, unset_jwt_cookies, verify_jwt_in_request, get_jwt, current_user
from sendgrid.helpers.mail import Mail

from ..models import Role, User, Ticket

from .. import db, jwt, mail

admin = Blueprint("admin", __name__)


def admin_required(refresh=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if refresh:
                verify_jwt_in_request(refresh=True)
                claims = get_jwt()
                if claims["auth_level"] == "admin":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)
            else:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["auth_level"] == "admin":
                    return fn(*args, **kwargs)
                else:
                    return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)

        return decorator

    return wrapper


@admin.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    admin_role = Role.query.filter_by(name='admin').first()
    admin_role_id = admin_role.id
    user_check = User.query.filter_by(username = username).first()
    if user_check:
        return make_response({"message": "user already exists"}, 401)
    elif username is None or password is None or email is None:
        return make_response({"message": "bad request"}, 400)
    new_admin = User(username = username, email = email, role = admin_role_id)
    new_admin.set_password(password=password)
    db.session.add(new_admin)
    db.session.commit()
    return make_response({"message": f"Admin {username} created"}, 201)

@admin.route('/login', methods = ['POST'])
def login():
    
    
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    admin_role = Role.query.filter_by(name='admin').first()
    admin_role_id = admin_role.id
    if user.role == admin_role_id:
        if user is None or not user.check_password(password):
            return make_response(jsonify({"msg": "Invalid username or password"}), 401)
        else:
            additional_claims = {"auth_level": "admin", "username": user.username}
            access_token = create_access_token(identity=user, additional_claims = additional_claims)
            refresh_token = create_refresh_token(identity=user, additional_claims = additional_claims)
            resp = make_response(jsonify({'access_token': access_token}))
            resp.set_cookie('refresh_token_cookie', refresh_token, httponly=True)
            resp.set_cookie('access_token_cookie', access_token, httponly=True)
            return resp, 200
    else:
        return make_response(jsonify({"msg": "UNAUTHORISED ACCESS"}), 401)


@admin.route('/logout', methods = ['POST'])
@admin_required()
def logout():
    resp = make_response(jsonify({'msg': 'Successfully logged out.'}), 200)
    unset_jwt_cookies(resp)
    return resp


@admin.route('/refresh', methods=['POST'])
@admin_required(refresh=True)
def refresh():
    current_admin_id = get_jwt_identity()
    current_admin = User.query.get(current_admin_id)
    additional_claims = {"auth_level": "admin", "username": current_admin.username}
    access_token = create_access_token(identity=current_user, additional_claims = additional_claims)
    resp = make_response(jsonify({'access_token': access_token}), 200)
    resp.set_cookie('access_token_cookie', access_token, httponly=True)
    
    return resp


@admin.route('/add-staff', methods = ['POST'])
@admin_required()
def add_staff():
    admin_id = get_jwt_identity()
    admin_user = User.query.filter_by(id = admin_id).first()
    staff_email = request.json.get('email')
    staff_username = request.json.get('username')
    staff_password = request.json.get('password')
    staff_check = User.query.filter_by(username = staff_username).first()
    if staff_check:
        return make_response({"message": "user already exists"}, 401)
    elif staff_username is None or staff_password is None or staff_email is None:
        return make_response({"message": "bad request"}, 400)
    staff_role = Role.query.filter_by(name='staff').first()
    staff_role_id = staff_role.id
    new_staff = User(username = staff_username, email = staff_email, role = staff_role_id)
    new_staff.set_password(staff_password)
    db.session.add(new_staff)
    db.session.commit()
    # msg = Message(f"username: {staff_username}, password: {staff_password}", recipients=[staff_email,])
    msg = Mail(
        from_email="abulaman6@gmail.com",
        to_emails=staff_email,
        subject="account created",
        plain_text_content=f"username: {staff_username}, password: {staff_password}"
    )
    mail.send(msg)
    return make_response({'message': f'staff {staff_username} added'})


@admin.route('/add-student', methods = ['POST'])
@admin_required()
def add_student():
    admin_id = get_jwt_identity()
    admin_user = User.query.filter_by(id = admin_id).first()
    student_email = request.json.get('email')
    student_username = request.json.get('username')
    student_password = request.json.get('password')
    student_check = User.query.filter_by(username = student_username).first()
    if student_check:
        return make_response({"message": "user already exists"}, 401)
    elif student_username is None or student_password is None or student_email is None:
        return make_response({"message": "bad request"}, 400)
    student_role = Role.query.filter_by(name='student').first()
    student_role_id = student_role.id
    new_student = User(username = student_username, email = student_email, role = student_role_id)
    new_student.set_password(student_password)
    db.session.add(new_student)
    db.session.commit()
    msg = Mail(
        from_email="abulaman6@gmail.com",
        to_emails=student_email,
        subject="account created",
        plain_text_content=f"username: {student_username}, password: {student_password}"
    )
    mail.send(msg)
    return make_response({'message': f'student {student_username} added'})

@admin.route('/delete-staff/<int:id>', methods = ['DELETE'])
@admin_required()
def delete_staff(id):
    admin_id = get_jwt_identity()
    admin_user = User.query.filter_by(id = admin_id)
    staff_check = User.query.filter_by(id = id).first()
    if staff_check:
        email = staff_check.email
        name = staff_check.username
        db.session.delete(staff_check)
        db.session.commit()
        msg = Mail(
        from_email="abulaman6@gmail.com",
        to_emails=email,
        subject="account deleted",
        plain_text_content=f"your account has been deleted by admin {admin_user.username}"
        )
        mail.send(msg)
        return make_response({"message": f"staff {name}'s account deleted "}, 204)
    return make_response({"message": "Staff doesn't exist"}, 404)

@admin.route('/change-password', methods = ['PUT'])
@admin_required
def change_password():
    admin_id = get_jwt_identity()
    password = request.json.get('password')
    if password is None:
        return make_response({"message": "bad request"}, 400)
    admin_user = User.query.filter_by(id = admin_id).first()
    admin_user.set_password(password)
    db.session.commit()
    return make_response({"message": "password changed successfully"}, 202)


@admin.route('/delete-ticket/<int:id>', methods = ['DELETE'])
@admin_required()
def delete_ticket(id):
    ticket_check = Ticket.query.filter_by(id = id).first()
    if ticket_check:
        db.session.delete(ticket_check)
        db.session.commit()
        return make_response({"message": "Ticket deleted successfully"}, 204)
    return make_response({"message": "ticket doesn't exist"}, 404)



@admin.route('/get-all-staff-stats', methods = ['GET'])
@admin_required()
def get_all_staff_stats():
    staff_role = Role.query.filter_by(name='staff').first()
    staff_role_id = staff_role.id
    all_staff = User.query.filter_by(role = staff_role_id).all()
    tickets_by_staff = {staff.username:{"id": staff.id ,"email": staff.email, "tickets": [ticket.to_dict() for ticket in staff.get_resolved_tickets()]} for staff in all_staff}

    return make_response(jsonify(tickets_by_staff), 200)


@admin.route('/get-staff-stats/<int:id>', methods = ['GET'])
@admin_required()
def get_staff_stats(id):
    staff_check = User.query.filter_by(id = id).first()
    if staff_check:
        tickets = [ticket.to_dict for ticket in staff_check.get_resolved_tickets()]
        return make_response(jsonify(tickets), 200)
    return make_response({"message": "Staff doesn't exist"}, 404)




