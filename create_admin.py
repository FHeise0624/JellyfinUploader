"""
Only run once to create first admin User account
"""
from app import app, db
from user.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    username = 'admin'
    password = 'your_secure_password'
    role = 'admin'

    if not User.query.filter_by(username=username).first():
        user = User(username=username, password=generate_password_hash(password), role=role)
        db.session.add(user)
        db.session.commit()
        print('Admin user created.')
    else:
        print('User already exists.')
