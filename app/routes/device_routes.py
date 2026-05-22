from flask import Blueprint
from app.controllers.device_controller import (
    get_devices, get_device, create_device, update_device, delete_device,
)
from app.middlewares.auth_guard import login_required

device_bp = Blueprint('devices', __name__, url_prefix='/api/devices')

device_bp.route('', methods=['GET'])(login_required(get_devices))
device_bp.route('', methods=['POST'])(login_required(create_device))
device_bp.route('/<int:device_id>', methods=['GET'])(login_required(get_device))
device_bp.route('/<int:device_id>', methods=['PUT'])(login_required(update_device))
device_bp.route('/<int:device_id>', methods=['DELETE'])(login_required(delete_device))
