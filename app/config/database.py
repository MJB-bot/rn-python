from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models.admin import Admin
        from app.models.employee import Employee
        from app.models.category import Category
        from app.models.device import Device
        db.create_all()
