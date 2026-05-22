from flask import request
from marshmallow import ValidationError
from app.schemas.category_schema import CategorySchema, CategoryUpdateSchema
from app.services import category_service
from app.utils.response import success, created, error


def get_categories():
    result = category_service.get_categories()
    return success(result)


def get_category(category_id):
    category = category_service.get_category_by_id(category_id)
    if not category:
        return error('分类不存在', 404)
    cats = category_service.get_categories()
    item = next((c for c in cats if c['id'] == category_id), category.to_dict())
    return success(item)


def create_category():
    try:
        data = CategorySchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    category, err = category_service.create_category(data)
    if err:
        return error(err, 400)

    return created(category.to_dict(), '创建成功')


def update_category(category_id):
    try:
        data = CategoryUpdateSchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    category, err = category_service.update_category(category_id, data)
    if err:
        if err == '分类不存在':
            return error(err, 404)
        return error(err, 400)

    return success(category.to_dict(), '更新成功')


def delete_category(category_id):
    _, err = category_service.delete_category(category_id)
    if err:
        if err == '分类不存在':
            return error(err, 404)
        return error(err, 400)
    return success(message='删除成功')


def get_category_devices(category_id):
    data = category_service.get_category_devices(category_id)
    if data is None:
        return error('分类不存在', 404)
    return success(data)
