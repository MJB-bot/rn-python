"""
Seed script: creates the default admin account.

Run:
  python seed.py
"""
from app.app import create_app
from app.config.database import db
from app.models.admin import Admin
from app.utils.password import hash_password


def seed():
    app = create_app()
    with app.app_context():
        existing = Admin.query.filter_by(username='admin').first()
        if existing:
            print('[SKIP] Default admin already exists.')
        else:
            admin = Admin(
                username='admin',
                password=hash_password('123456'),
                role='admin',
            )
            db.session.add(admin)
            db.session.commit()
            print('[OK] Default admin created (username: admin, password: 123456)')


if __name__ == '__main__':
    seed()
