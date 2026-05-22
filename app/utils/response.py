from flask import jsonify


def success(data=None, message='success'):
    body = {'success': True, 'message': message}
    if data is not None:
        body['data'] = data
    return jsonify(body)


def error(message='error', status_code=400):
    body = {'success': False, 'message': message}
    return jsonify(body), status_code


def created(data=None, message='创建成功'):
    body = {'success': True, 'message': message}
    if data is not None:
        body['data'] = data
    return jsonify(body), 201
