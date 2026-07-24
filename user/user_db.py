from user.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

def get_user_by_id(user_id):
    return db.session.get(User, int(user_id))

def get_all_users():
    return User.query.all()

def get_user(username):
    return User.query.filter_by(username=username).first()

def new_user(username, password, role):
    hashed_password = generate_password_hash(password)

    if role == "admin":
        final_role = "admin"
    elif role == "child":
        final_role = "child"
    else:
        final_role = "user"

    user = User(username=username, password=hashed_password, role=final_role)
    db.session.add(user)
    db.session.commit()

def delete_user(userid):
    user = db.session.get(User, int(userid))
    if user:
        db.session.delete(user)
        db.session.commit()

def verify_password(user, password):
    return check_password_hash(user.password, password)