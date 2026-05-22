from flask import request
from marshmallow import ValidationError
from app.schemas.device_schema import DeviceSchema, DeviceUpdateSchema, DeviceQuerySchema
from app.services import device_service
from app.utils.response import success, created, error


def get_devices():
    try:
        params = DeviceQuerySchema().load(request.args)
    except ValidationError as e:
        return error(str(e.messages), 400)

    result = device_service.get_devices(
        page=params['page'],
        page_size=params['page_size'],
        category_id=params.get('category_id'),
        name=params.get('name'),
    )
    return success(result)


def get_device(device_id):
    device = device_service.get_device_by_id(device_id)
    if not device:
        return error('设备不存在', 404)
    return success(device.to_dict())


def create_device():
    try:
        data = DeviceSchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    device, err = device_service.create_device(data)
    if err:
        return error(err, 400)

    return created(device.to_dict(), '创建成功')


def update_device(device_id):
    try:
        data = DeviceUpdateSchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    device, err = device_service.update_device(device_id, data)
    if err:
        if err == '设备不存在':
            return error(err, 404)
        return error(err, 400)

    return success(device.to_dict(), '更新成功')


def delete_device(device_id):
    _, err = device_service.delete_device(device_id)
    if err:
        return error(err, 404)
    return success(message='删除成功')
