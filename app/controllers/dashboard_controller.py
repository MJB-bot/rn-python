from app.services import dashboard_service
from app.utils.response import success


def get_stats():
    data = dashboard_service.get_stats()
    return success(data)
