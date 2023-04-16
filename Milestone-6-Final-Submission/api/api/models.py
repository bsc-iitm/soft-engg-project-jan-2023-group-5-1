from . import db
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), nullable = False)
    description = db.Column(db.String(64))
    user_ref = db.relationship('User', cascade='all, delete-orphan', backref='role_registered')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(600), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    dp = db.Column(db.String(255), default = "default_dp.png", nullable = False)
    created_at = db.Column(db.DateTime(timezone = True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(), default=func.now(), onupdate=func.now(), nullable=False)
    issued_tickets = db.relationship('Ticket', foreign_keys='Ticket.issuer' , backref='created_by', lazy='select')
    resolved_tickets = db.relationship('Ticket', backref='resolved_by', foreign_keys='Ticket.resolver', lazy='select')
    

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


    def get_issued_tickets(self):
        return Ticket.query.filter_by(created_by=self).all()
    def get_resolved_tickets(self):
        return Ticket.query.filter_by(resolved_by=self).all()
    
    def to_dict(self):
        r = {
                "id": self.id,
                "email": self.email,
                "username": self.username,
                "role": self.role,
                "dp": self.dp,
                "created_at": self.created_at,
                "updated_at": self.updated_at
            }
        return r








class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    issued_at = db.Column(db.DateTime(), default=func.now(), nullable=False)
    solution = db.Column(db.Text())
    user_attachments = db.Column(db.ARRAY(db.String(255)))
    staff_attachments = db.Column(db.ARRAY(db.String(255)))
    is_resolved = db.Column(db.Boolean(), default=False, nullable=False)
    resolved_at = db.Column(db.DateTime())
    one_up = db.Column(db.Integer(), default = 0)
    issuer = db.Column(db.Integer(), db.ForeignKey('user.id'))
    resolver = db.Column(db.Integer(), db.ForeignKey('user.id'))
    faq_ref = db.relationship('Faq', cascade='all, delete-orphan', backref='ticket_ref')

    def __repr__(self):
        return f'<Ticket {self.id} - {self.title}>'

    @classmethod
    def from_dict(cls, data):
        ticket = cls()
        ticket.title = data.get("title")
        ticket.body = data.get("body")
        ticket.issuer = data.get("user_id")
        ticket.user_attachments = data.get("user_attachments")
        return ticket

    def to_dict(self):
        r = {

                "id": self.id,
                "title": self.title,
                "body": self.body,
                "issued_at": self.issued_at,
                "issuer": self.created_by.to_dict(),
                "solution": self.solution,
                "user_attachments": self.user_attachments,
                "staff_attachments": self.staff_attachments,
                "is_resolved": self.is_resolved,
                "resolved_at": self.resolved_at,
                "resolver": self.resolved_by.to_dict() if self.resolved_by else None,
                "one_up": self.one_up,


             }
        return r


class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer(), db.ForeignKey('ticket.id'))

    def to_dict(self):
        r = {
                "id": self.id,
                "ticket_id": self.ticket_id,
                "ticket": self.ticket_ref.to_dict()
            }
        return r


