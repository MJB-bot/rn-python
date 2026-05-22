from functools import wraps
from flask import request, g
from app.config.jwt_config import decode_token
from app.utils.response import error
import jwt


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return error('未授权，请重新登录', 401)

        token = auth_header.split('Bearer ')[-1].strip()
        if not token:
            return error('未授权，请重新登录', 401)

        try:
            payload = decode_token(token)
            g.current_admin = payload
        except jwt.ExpiredSignatureError:
            return error('登录已过期，请重新登录', 401)
        except jwt.InvalidTokenError:
            return error('未授权，请重新登录', 401)

        return f(*args, **kwargs)

    return decorated
