from flask import Blueprint
from app.controllers.employee_controller import (
    get_employees, get_employee, create_employee, update_employee, delete_employee,
)
from app.middlewares.auth_guard import login_required

employee_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

employee_bp.route('', methods=['GET'])(login_required(get_employees))
employee_bp.route('', methods=['POST'])(login_required(create_employee))
employee_bp.route('/<int:employee_id>', methods=['GET'])(login_required(get_employee))
employee_bp.route('/<int:employee_id>', methods=['PUT'])(login_required(update_employee))
employee_bp.route('/<int:employee_id>', methods=['DELETE'])(login_required(delete_employee))
