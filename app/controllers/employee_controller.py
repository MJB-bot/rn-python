from flask import request
from marshmallow import ValidationError
from app.schemas.employee_schema import EmployeeSchema, EmployeeUpdateSchema, EmployeeQuerySchema
from app.services import employee_service
from app.utils.response import success, created, error


def get_employees():
    try:
        params = EmployeeQuerySchema().load(request.args)
    except ValidationError as e:
        return error(str(e.messages), 400)

    result = employee_service.get_employees(
        page=params['page'],
        page_size=params['page_size'],
        name=params.get('name'),
    )
    return success(result)


def get_employee(employee_id):
    employee = employee_service.get_employee_by_id(employee_id)
    if not employee:
        return error('员工不存在', 404)
    return success(employee.to_dict())


def create_employee():
    try:
        data = EmployeeSchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    employee, err = employee_service.create_employee(data)
    if err:
        return error(err, 400)

    return created(employee.to_dict(), '创建成功')


def update_employee(employee_id):
    try:
        data = EmployeeUpdateSchema().load(request.json or {})
    except ValidationError as e:
        return error(str(e.messages), 400)

    employee, err = employee_service.update_employee(employee_id, data)
    if err:
        if err == '员工不存在':
            return error(err, 404)
        return error(err, 400)

    return success(employee.to_dict(), '更新成功')


def delete_employee(employee_id):
    _, err = employee_service.delete_employee(employee_id)
    if err:
        return error(err, 404)
    return success(message='删除成功')
