from functools import wraps
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import numpy as np

from ..models import Faq, Ticket, Role, User
from .. import db, model

from ..decorators import student_required, staff_required



ticket = Blueprint("ticket", __name__)



@ticket.route('/', methods = ['GET'])
@jwt_required()
def get_tickets():
    tickets = Ticket.query.order_by(Ticket.issued_at.desc()).all()
    tickets_dict_list = [ticket.to_dict() for ticket in tickets]
    return make_response(jsonify(tickets_dict_list), 200)



@ticket.route('/<int:id>', methods = ['GET'])
@jwt_required()
def get_one(id):
    ticket = Ticket.query.filter_by(id = id).first()
    if ticket:
        return make_response(jsonify(ticket.to_dict()), 200)
    return make_response({"message": "ticket not found"}, 404)








@ticket.route('/issue-ticket', methods = ['POST'])
@student_required()
def issue_ticket():
    student_id = get_jwt_identity()
    json = request.json
    data = dict(json)
    data["user_id"] = student_id
    new_ticket = Ticket.from_dict(data)
    db.session.add(new_ticket)
    db.session.commit()
    return make_response({"message": "ticket added successfully"}, 201)


@ticket.route('/get-similar', methods = ['POST'])
# @student_required()
def get_similar_tickets():
    title = request.json.get('title')
    query_vector = model.encode(title)
    tickets = Ticket.query.all()
    ticket_vectors = [model.encode(ticket.title) for ticket in tickets]
    similarities = np.dot(ticket_vectors, query_vector.T)
    if len(similarities) < 5:
        top_indices = np.argsort(similarities, axis=0)[::-1][:len(similarities)]
    else:
        top_indices = np.argsort(similarities, axis=0)[::-1][:5]
    similar_tickets = [tickets[i] for i in top_indices]
    similar_tickets_dict_list = [ticket.to_dict() for ticket in similar_tickets]
    return make_response(jsonify(similar_tickets_dict_list), 200)


@ticket.route('/resolve/<int:id>', methods = ['PUT'])
@staff_required()
def resolve(id):
    staff_id = get_jwt_identity()
    ticket = Ticket.query.filter_by(id = id).first()
    json = request.json
    solution = json.get('solution')
    staff_attachments = json.get('staff_attachments')
    if ticket:
        ticket.solution = solution
        ticket.staff_attachments = staff_attachments
        ticket.is_resolved = True
        ticket.resolver = staff_id
        db.session.commit()
        return make_response({"message": "ticket resolved successfully"}, 200)
    return make_response({"message": "ticket not found"}, 404)


@ticket.route('/delete/<int:id>',methods = ['DELETE'])
@student_required()
def delete_ticket(id):
    student_id = get_jwt_identity()
    ticket = Ticket.query.filter_by(id = id).first()
    if ticket:
        if ticket.issuer == student_id:
            db.session.delete(ticket)
            db.session.commit()
            return make_response({'message': 'ticket deleted successfully'}, 204)
        return make_response({"message": "Unauthorized access"}, 401)
    return make_response({"message": "ticket doesn't exist"}, 404)


@ticket.route('/one-up/<int:id>', methods = ['POST'])
@student_required()
def one_up(id):
    student_id = get_jwt_identity()
    ticket_check = Ticket.query.filter_by(id = id).first()
    if ticket_check:
        if ticket_check.issuer == student_id:
            return make_response({"message": "You can't One up yourself"}, 400)
        ticket_check.one_up += 1
        db.session.commit()
        return make_response({"message": "ticket one upped succesfully"}, 200)
    return make_response({"message": "ticket doesn't exist"}, 404)


@ticket.route('/get-all-issues', methods = ['GET'])
@student_required()
def get_all_issues():
    student_id = get_jwt_identity()
    student = User.query.filter_by(id = student_id).first()
    tickets = [ticket.to_dict() for ticket in student.get_issued_tickets()]
    # print(tickets)
    return make_response(jsonify(tickets), 200)


@ticket.route('/get-all-resolves', methods = ['GET'])
@staff_required()
def get_all_resolves():
    staff_id = get_jwt_identity()
    staff = User.query.filter_by(id = staff_id).first()
    tickets = [ticket.to_dict() for ticket in staff.get_resolved_tickets()]
    return make_response(jsonify(tickets), 200)





@ticket.route('/add-faq/<int:id>', methods=['POST'])
@staff_required
def add_faq(id):
    ticket = Ticket.query.filter_by(id=id).first()
    if ticket:
        faq = Faq(ticket_id = id)
        db.session.add(faq)
        db.session.commit()
        return make_response({"message": "FAQ added successfully"}, 201)
    return make_response({"message": "Ticket not found"}, 404)


@ticket.route('/get-all-faqs', methods=['GET'])
def get_all_faqs():
    faqs = Faq.query.all()
    faqs_dict_list = [faq.to_dict() for faq in faqs]
    return make_response(jsonify(faqs_dict_list), 200)

@ticket.route('/get-faq/<int:id>', methods=['GET'])
def get_faq(id):
    faq = Faq.query.filter_by(ticket_id=id).first()
    if faq:
        return make_response(jsonify(faq.to_dict()), 200)
    return make_response({"message": "FAQ not found"}, 404)