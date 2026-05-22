from flask import Blueprint
from app.controllers.dashboard_controller import get_stats
from app.middlewares.auth_guard import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

dashboard_bp.route('/stats', methods=['GET'])(login_required(get_stats))
