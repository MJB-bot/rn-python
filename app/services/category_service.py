from app.models.category import Category
from app.config.database import db
from sqlalchemy import func


def get_categories():
    categories = (
        db.session.query(
            Category,
            func.count('devices.id').label('device_count'),
        )
        .outerjoin(Category.devices)
        .group_by(Category.id)
        .order_by(Category.created_at.desc())
        .all()
    )
    result = []
    for cat, count in categories:
        item = cat.to_dict()
        item['device_count'] = count
        result.append(item)
    return result


def get_category_by_id(category_id):
    return Category.query.get(category_id)


def create_category(data):
    existing = Category.query.filter_by(name=data['name']).first()
    if existing:
        return None, '分类名称已存在'
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return category, None


def update_category(category_id, data):
    category = Category.query.get(category_id)
    if not category:
        return None, '分类不存在'

    existing = Category.query.filter(Category.name == data['name'], Category.id != category_id).first()
    if existing:
        return None, '分类名称已存在'

    category.name = data['name']
    db.session.commit()
    return category, None


def delete_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return None, '分类不存在'

    if category.devices.count() > 0:
        return None, '分类下存在设备，无法删除'

    db.session.delete(category)
    db.session.commit()
    return True, None


def get_category_devices(category_id):
    category = Category.query.get(category_id)
    if not category:
        return None
    return {
        'category': category.to_dict(),
        'devices': [d.to_dict() for d in category.devices.all()],
    }
