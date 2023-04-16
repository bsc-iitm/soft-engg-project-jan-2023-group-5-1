from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sendgrid import SendGridAPIClient
from sentence_transformers import SentenceTransformer
from flask_migrate import Migrate



db = SQLAlchemy()
jwt = JWTManager()
mail = SendGridAPIClient("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")
model = SentenceTransformer('paraphrase-distilroberta-base-v2')
migrate = Migrate()


DB_NAME = "project.sqlite3"

def create_app():
    app = Flask(__name__)
    app.config['FLASK_DEBUG'] = True
    app.config['SECRET_KEY'] = 'SJDFGWIFUIWVUEVFYVWEUBFVYWEVFWEFV'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://abulaman:ufv531sFidCUrAojzIawCwS4hyiQlgQu@dpg-cg87mn5269vf27f4sq30-a.oregon-postgres.render.com/ticket_support_inz4"

    app.config['JWT_SECRET_KEY'] = 'abulaman'  # Change this to a secure secret key in production
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60  # 1 hour
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 7 * 24 * 60 * 60  # 7 days
    # app.config['MAIL_SENDGRID_API_KEY'] = "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"
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    CORS(app)

    from .views import views
    from .admin.views import admin
    from .staff.views import staff
    from .student.views import student
    from .ticket.views import ticket
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(admin, url_prefix = '/admin')
    app.register_blueprint(staff, url_prefix = '/staff')
    app.register_blueprint(student, url_prefix = '/student')
    app.register_blueprint(ticket, url_prefix = '/ticket')


    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'  # allow credentials
        return response

    from .models import User

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()


    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id



    with app.app_context():
        from .models import User, Ticket, Role, Faq
        db.create_all()
    with app.app_context():
        app.model = SentenceTransformer('paraphrase-distilroberta-base-v2')


    return app
