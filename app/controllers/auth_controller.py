from flask import request
from marshmallow import ValidationError
from app.schemas.auth_schema import LoginSchema
from app.services import auth_service
from app.utils.response import success, error


def login():
    try:
        data = LoginSchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    result, err = auth_service.login(data['username'], data['password'])
    if err:
        return error(err, 401)

    return success(result, '登录成功')
