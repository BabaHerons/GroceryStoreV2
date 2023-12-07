from src import api, db
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Cart, Product, Category
from src.utils import args, current_date_time

fields = ["product_id", "user_id", "quantity"]
product_args = args(fields)
product_patch_args = args(["quantity"])

class CartEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers and "user_id" in request.headers:
            role = request.headers["role"]
            user_id = request.headers["user_id"]
            if role == "user":
                cart = [
                    {**i[0].output, **{"name":i.name, "price":i.price, "unit":i.unit, "category":i.title}}
                    for i in Cart.query.filter_by(user_id = user_id)
                    .join(Product, Cart.product_id == Product.id)
                    .add_columns(Product.name, Product.price, Product.unit)
                    .join(Category, Product.category_id == Category.id)
                    .add_columns(Category.title)
                    .all()
                ]
                return cart
            return {"message":"Not Allowed"}, 401
        return {"message":"Missing values in Headers."}, 400
    
    @token_required
    def post(self):
        args = product_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role == "user":
                args["date"] = current_date_time()
                product = Cart(**args)
                db.session.add(product)
                db.session.commit()
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401

    # FOR UPDATING QUANTITY OF A PRODUCT IN CART
    @token_required
    def patch(self):
        args = product_patch_args.parse_args()
        if "role" in request.headers and "id" in request.args:
            role = request.headers["role"]
            id = request.args["id"]
            if role == "user":
                product = Cart.query.filter_by(id = id).first()
                if not product:
                    return {"message":"Product not found in Cart."}, 404
                product.date = current_date_time()
                product.quantity = args["quantity"]
                db.session.add(product)
                db.session.commit()
                return {"message":"Quantity updated successfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def delete(self):
        if "role" in request.headers and "id" in request.args:
            role = request.headers["role"]
            cart_id = request.args["id"]
            if role == "user":
                product = Cart.query.filter_by(id = cart_id).first()
                if not product:
                    return {"message":"Item not found in cart."}, 404
                db.session.delete(product)
                db.session.commit()
                return {"message":"Deleted successfully"}
        return {"message":"Not Allowed"}, 401


api.add_resource(CartEndpoint, "/cart")