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
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    created_by_name = db.Column(db.String(100), db.ForeignKey('user.full_name'), nullable=False)
    request_status = db.Column(db.Boolean(), nullable=False, default=False)

    @property
    def output(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_active":self.is_active,
            "created_by": self.created_by,
            "created_by_name": self.created_by_name,
            "request_status": self.request_status,
        }

class CategoryChangeRequest(db.Model):
    __tablename__ = "category_change_request"
    id = db.Column(db.Integer(), primary_key = True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    created_by_name = db.Column(db.String(100), db.ForeignKey('user.full_name'), nullable=False)
    for_category = db.Column(db.Integer(), db.ForeignKey("category.id"), nullable=False)
    request_type = db.Column(db.String(100), nullable=False)  # edit, delete
    status = db.Column(db.String(100), nullable=False)        # approved, declined, pending

    @property
    def output(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "for_category":self.for_category,
            "created_by": self.created_by,
            "created_by_name": self.created_by_name,
            "request_type": self.request_type,
            "status": self.status,
        }