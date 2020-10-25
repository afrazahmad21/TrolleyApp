import bcrypt

from Q2.User.model import User


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def check_user(email, password):
    found = False
    body = {
        'email': email
    }
    user = User.objects.get(**body)
    if not user:
        message = 'email not found'
        return found, message
    user = user.to_json()
    if bcrypt.checkpw(password.encode("utf-8"), user['password'].encode('utf-8')):
        found = True
        message = 'found successfully'
    else:
        message = 'Incorrect password'

    return found, message


def init_user():
    count = User.objects.count()

    if not count:
        new_user = User(
            email="test@email.com",
            password=hash_password("password")
        )

        new_user.save()
