from app.models.device import Device
from app.models.category import Category
from app.config.database import db
from sqlalchemy import desc


def get_devices(page=1, page_size=10, category_id=None, name=None):
    query = Device.query
    if category_id:
        query = query.filter(Device.category_id == category_id)
    if name:
        query = query.filter(Device.name.like(f'%{name}%'))
    query = query.order_by(desc(Device.created_at))
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    return {
        'list': [d.to_dict() for d in pagination.items],
        'total': pagination.total,
    }


def get_device_by_id(device_id):
    return Device.query.get(device_id)


def create_device(data):
    category = Category.query.get(data['category_id'])
    if not category:
        return None, '分类不存在'
    device = Device(
        name=data['name'],
        model=data.get('model'),
        category_id=data['category_id'],
    )
    db.session.add(device)
    db.session.commit()
    return device, None


def update_device(device_id, data):
    device = Device.query.get(device_id)
    if not device:
        return None, '设备不存在'

    category = Category.query.get(data['category_id'])
    if not category:
        return None, '分类不存在'

    device.name = data['name']
    device.model = data.get('model')
    device.category_id = data['category_id']
    db.session.commit()
    return device, None


def delete_device(device_id):
    device = Device.query.get(device_id)
    if not device:
        return None, '设备不存在'
    db.session.delete(device)
    db.session.commit()
    return True, None
