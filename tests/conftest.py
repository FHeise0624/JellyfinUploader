import pytest
from werkzeug.security import generate_password_hash

from app import app as flask_app
from user.models import db, User


@pytest.fixture()
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'PHOTOS_UPLOAD_ENABLED': False,
        'WTF_CSRF_ENABLED': False,
    })

    with flask_app.app_context():
        db.create_all()

        admin = User(username='admin', password=generate_password_hash('adminpass'), role='admin')
        user  = User(username='user',  password=generate_password_hash('userpass'),  role='user')
        db.session.add_all([admin, user])
        db.session.commit()

    yield flask_app

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_client(client):
    """Authenticated client with admin role."""
    client.post('/login', data={'username': 'admin', 'password': 'adminpass'})
    return client


@pytest.fixture()
def user_client(client):
    """Authenticated client with regular user role."""
    client.post('/login', data={'username': 'user', 'password': 'userpass'})
    return client
