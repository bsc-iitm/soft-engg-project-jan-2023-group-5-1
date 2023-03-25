import pytest
from api import create_app, db
from api.models import User, Role, Ticket
from api.decorators import admin_required, staff_required, student_required
from flask import url_for
import json

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/test_db'
    app.config['TESTING'] = True
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            # create test data
            admin_role = Role(name='Admin')
            staff_role = Role(name='Staff')
            student_role = Role(name='Student')
            db.session.add_all([admin_role, staff_role, student_role])
            admin_user = User(username='admin', password='admin', email='admin@admin.com', role=admin_role)
            staff_user = User(username='staff', password='staff', email='staff@staff.com', role=staff_role)
            student_user = User(username='student', password='student', email='student.student.com', role=student_role)
            db.session.add_all([admin_user, staff_user, student_user])
            ticket = Ticket(title='Test Ticket', description='Test Description', user=student_user)
            db.session.add(ticket)
            db.session.commit()

        yield testing_client

        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def access_token_admin(test_client):
    response = test_client.post(url_for('admin.login'), json={
        'username': 'admin',
        'password': 'admin'
    })
    json_data = json.loads(response.data.decode())
    return json_data['access_token']


@pytest.fixture(scope='module')
def access_token_staff(test_client):
    response = test_client.post(url_for('staff.login'), json={
        'username': 'staff',
        'password': 'staff'
    })
    json_data = json.loads(response.data.decode())
    return json_data['access_token']


@pytest.fixture(scope='module')
def access_token_student(test_client):
    response = test_client.post(url_for('student.login'), json={
        'username': 'student',
        'password': 'student'
    })
    json_data = json.loads(response.data.decode())
    return json_data['access_token']



def test_admin_required(test_client, access_token_admin):
    response = test_client.get(url_for('admin.get_all_staff_stats'), headers={
        'Cookie': f'access_token_cookie={access_token_admin}'
    })
    assert response.status_code == 200


def test_staff_required(test_client, access_token_staff):
    response = test_client.get(url_for('tickets.get_all_resolves'), headers={
        'Cookie': f'access_token_cookie={access_token_staff}'
    })
    assert response.status_code == 200


def test_student_required(test_client, access_token_student):
    response = test_client.get(url_for('tickets.get_all_issues'), headers={
        'Cookie': f'access_token_cookie={access_token_student}'
    })
    assert response.status_code == 200


def test_admin_refresh_tokens(test_client):
    # get access and refresh token
    response = test_client.post(url_for('admin.login'), json={
        'username': 'admin',
        'password': 'admin'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    refresh_token = response.cookies.get('refresh_token_cookie')

    # refresh access token
    response = test_client.post(url_for('admin.refresh'), headers={
        'Cookie': f'access_token_cookie={access_token}; refresh_token_cookie={refresh_token}'
    })
    json_data = json.loads(response.data.decode())
    assert 'access_token' in json_data

    # ensure new access token is different from old one
    new_access_token = json_data['access_token']
    assert new_access_token != access_token

def test_staff_refresh_tokens(test_client):
    # get access and refresh token
    response = test_client.post(url_for('staff.login'), json={
        'username': 'staff',
        'password': 'staff'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    refresh_token = response.cookies.get('refresh_token_cookie')

    # refresh access token
    response = test_client.post(url_for('staff.refresh'), headers={
        'Cookie': f'access_token_cookie={access_token}; refresh_token_cookie={refresh_token}'
    })
    json_data = json.loads(response.data.decode())
    assert 'access_token' in json_data

    # ensure new access token is different from old one
    new_access_token = json_data['access_token']
    assert new_access_token != access_token


def test_student_refresh_tokens(test_client):
    # get access and refresh token
    response = test_client.post(url_for('student.login'), json={
        'username': 'student',
        'password': 'student'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    refresh_token = response.cookies.get('refresh_token_cookie')

    # refresh access token
    response = test_client.post(url_for('student.refresh'), headers={
        'Cookie': f'access_token_cookie={access_token}; refresh_token_cookie={refresh_token}'
    })
    json_data = json.loads(response.data.decode())
    assert 'access_token' in json_data

    # ensure new access token is different from old one
    new_access_token = json_data['access_token']
    assert new_access_token != access_token

def test_admin_change_password(test_client):
    # login as admin
    response = test_client.post(url_for('admin.login'), json={
        'username': 'admin',
        'password': 'admin'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    refresh_token = response.cookies.get('refresh_token_cookie')

    # change admin password
    response = test_client.post(url_for('admin.change_password'), headers={
        'Cookie': f'access_token_cookie={access_token}'
    }, json={
        'password': 'new_password'
    })
    assert response.status_code == 200

def test_staff_change_password(test_client):
    # login as admin
    response = test_client.post(url_for('staff.login'), json={
        'username': 'staff',
        'password': 'staff'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    refresh_token = response.cookies.get('refresh_token_cookie')

    # change admin password
    response = test_client.post(url_for('staff.change_password'), headers={
        'Cookie': f'access_token_cookie={access_token}'
    }, json={
        'password': 'new_password'
    })
    assert response.status_code == 200

def test_student_change_password(test_client):
    # login as admin
    response = test_client.post(url_for('student.login'), json={
        'username': 'student',
        'password': 'student'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    refresh_token = response.cookies.get('refresh_token_cookie')

    # change admin password
    response = test_client.post(url_for('student.change_password'), headers={
        'Cookie': f'access_token_cookie={access_token}'
    }, json={
        'password': 'new_password'
    })
    assert response.status_code == 200

def test_issue_ticket(test_client):
    response = test_client.post(url_for('student.login'), json={
        'username': 'student',
        'password': 'student'
    })
    json_data = json.loads(response.data.decode())
    access_token = json_data['access_token']
    response = test_client.post(url_for('ticket.issue_ticket'), headers={
        'Cookie': f'access_token_cookie={access_token}'
    } ,json={'title': 'New Ticket', 'body': 'New Ticket Description', 'user_attachments': []})
    assert response.status_code == 200

def test_resolve_ticket(test_client):

    # login as staff
    response = test_client.post(url_for('staff.login'), json={'username': 'staff', 'password': 'staff'})
    access_token = response.cookies.get('access_token')

    response = test_client.put(url_for('ticket.resolve', id=1), json={'solution': 'Resolved', 'staff_attachments': []}, cookies={'access_token': access_token})
    assert response.status_code == 200
