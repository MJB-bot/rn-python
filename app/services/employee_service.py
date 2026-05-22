from app.models.employee import Employee
from app.config.database import db
from sqlalchemy import desc


def get_employees(page=1, page_size=10, name=None):
    query = Employee.query
    if name:
        query = query.filter(Employee.name.like(f'%{name}%'))
    query = query.order_by(desc(Employee.created_at))
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    return {
        'list': [e.to_dict() for e in pagination.items],
        'total': pagination.total,
    }


def get_employee_by_id(employee_id):
    return Employee.query.get(employee_id)


def create_employee(data):
    existing = Employee.query.filter_by(email=data['email']).first()
    if existing:
        return None, '邮箱已被使用'
    employee = Employee(
        name=data['name'],
        age=data['age'],
        email=data['email'],
    )
    db.session.add(employee)
    db.session.commit()
    return employee, None


def update_employee(employee_id, data):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, '员工不存在'

    existing = Employee.query.filter(Employee.email == data['email'], Employee.id != employee_id).first()
    if existing:
        return None, '邮箱已被其他员工使用'

    employee.name = data['name']
    employee.age = data['age']
    employee.email = data['email']
    db.session.commit()
    return employee, None


def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return None, '员工不存在'
    db.session.delete(employee)
    db.session.commit()
    return True, None
