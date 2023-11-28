from src import db
import time

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key = True, nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    @property
    def output(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "is_active":self.is_active
        }

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer(), primary_key = True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    @property
    def output(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_active":self.is_active
        }