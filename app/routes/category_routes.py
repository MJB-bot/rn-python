from flask import Blueprint
from app.controllers.category_controller import (
    get_categories, get_category, create_category, update_category, delete_category,
    get_category_devices,
)
from app.middlewares.auth_guard import login_required

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

category_bp.route('', methods=['GET'])(login_required(get_categories))
category_bp.route('', methods=['POST'])(login_required(create_category))
category_bp.route('/<int:category_id>', methods=['GET'])(login_required(get_category))
category_bp.route('/<int:category_id>', methods=['PUT'])(login_required(update_category))
category_bp.route('/<int:category_id>', methods=['DELETE'])(login_required(delete_category))
category_bp.route('/<int:category_id>/devices', methods=['GET'])(login_required(get_category_devices))
