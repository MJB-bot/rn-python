from app.models.admin import Admin
from app.utils.password import check_password
from app.config.jwt_config import generate_token


def login(username, password):
    admin = Admin.query.filter_by(username=username).first()
    if not admin:
        return None, '用户名或密码错误'

    if not check_password(password, admin.password):
        return None, '用户名或密码错误'

    token = generate_token(admin.id, admin.username, admin.role)
    return {'token': token, 'admin': admin.to_dict()}, None
