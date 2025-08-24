from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(64), nullable=False, default='user')

    def is_admin(self):
        return self.role == 'admin'

    def is_child(self):
        return self.role == 'child'

    def get_username(self):
        return self.username

    def get_role(self):
        return self.role