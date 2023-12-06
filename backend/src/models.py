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
    request_status = db.Column(db.Boolean(), nullable=False, default=False)

    @property
    def output(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_active":self.is_active,
            "created_by": self.created_by,
            "request_status": self.request_status,
        }

class CategoryChangeRequest(db.Model):
    __tablename__ = "category_change_request"
    id = db.Column(db.Integer(), primary_key = True, nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
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
            "request_type": self.request_type,
            "status": self.status,
        }

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.String(200), primary_key = True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"), nullable=False)
    image = db.Column(db.String(500))
    m_date = db.Column(db.DateTime(), nullable=False)
    e_date = db.Column(db.DateTime(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False, default=0)
    price = db.Column(db.Integer(), nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    @property
    def output(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "image": self.image,
            "m_date": self.m_date.strftime("%d-%m-%Y"),
            "e_date": self.e_date.strftime("%d-%m-%Y"),
            "stock": self.stock,
            "price": self.price,
            "unit": self.unit,
            "created_by": self.created_by
        }

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer(), primary_key = True, nullable=False, unique=True)
    product_id = db.Column(db.String(200), db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)

    @property
    def output(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "user_id": self.user_id,
            "category": self.category,
            "quantity": self.quantity,
            "date": self.date.strftime("%d-%m-%Y, %H:%M:%S.%f")
        }

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.String(200), primary_key = True, nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    amount = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    
    @property
    def output(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.strftime("%d-%m-%Y, %H:%M:%S.%f"),
            "amount": self.amount,
            "status": self.status,
        }

