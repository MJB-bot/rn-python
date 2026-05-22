from app.config.database import db


class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
