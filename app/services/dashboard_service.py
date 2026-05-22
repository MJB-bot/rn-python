from app.models.employee import Employee
from app.models.category import Category
from app.models.device import Device


def get_stats():
    return {
        'employee_count': Employee.query.count(),
        'category_count': Category.query.count(),
        'device_count': Device.query.count(),
    }
