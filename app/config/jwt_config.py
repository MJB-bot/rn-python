import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_token(admin_id, username, role):
    payload = {
        'admin_id': admin_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS']),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM'],
    )
    return token


def decode_token(token):
    return jwt.decode(
        token,
        current_app.config['JWT_SECRET'],
        algorithms=[current_app.config['JWT_ALGORITHM']],
    )
