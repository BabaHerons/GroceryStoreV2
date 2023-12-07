from src import api, db, cache
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Product, Category
from src.utils import args, current_date_time_to_id
from flask_sse import sse
from src.custom_cache import get_all_product, get_all_product_by_sm
from datetime import datetime

fields = ["name", "description", "category_id", "m_date", "e_date",
          "stock", "price", "unit", "created_by"]
product_post_args = args(fields)
product_put_args = args(fields + ["id"])

class ProductEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers and "user_id" in request.headers:
            role = request.headers["role"]
            user_id = request.headers["user_id"]
            if role == "admin" or role == "user":
                if "id" in request.args:
                    product_id = request.args["id"]
                    product = Product.query.filter_by(id=product_id).first()
                    return product.output
                products = get_all_product()
                return products
            elif role == "store_admin":
                products = get_all_product_by_sm(user_id)
                return products
            return {"message":"Not Allowed"}, 401
        return {"message":"Missing values in Headers."}, 400

    @token_required
    def post(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["store_admin","admin"]:
                args = product_post_args.parse_args()
                args["id"] = f"PROD{current_date_time_to_id()}"
                args["m_date"] = datetime.strptime(args["m_date"], '%Y-%m-%d')
                args["e_date"] = datetime.strptime(args["e_date"], '%Y-%m-%d')
                product = Product(**args)
                db.session.add(product)
                db.session.commit()

                category = Category.query.filter_by(id = args["category_id"]).first()
                # SENDING NOTIFICATION TO USER ABOUT NEW ADDITION OF PRODUCT
                sse.publish({"message":f"New product {args['name'].upper()} has been added to category {category.title.upper()}"}, type="product")
                
                # DELETING THE OLD CACHE
                cache.delete("get_all_product")
                cache.delete_memoized(get_all_product_by_sm, args["created_by"])
                return {"message":"Product added successfully."}
        return {"message":"Not Allowed"}, 402
    
    @token_required
    def put(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["store_admin","admin"]:
                args = product_put_args.parse_args()
                args["m_date"] = datetime.strptime(args["m_date"], '%Y-%m-%d')
                args["e_date"] = datetime.strptime(args["e_date"], '%Y-%m-%d')
                product = Product.query.filter_by(id=args["id"]).first()
                if not product:
                    return {"message":"No products found."}, 404
                old_stock = product.stock

                if str(product.created_by) == str(args["created_by"]):
                    for key, value in args.items():
                        if key in fields and value is not None:
                            if key != "created_by":
                                setattr(product, key, value)
                    db.session.add(product)
                    db.session.commit()

                category = Category.query.filter_by(id = args["category_id"]).first()
                # SENDING NOTIFICATION TO USER ABOUT OUT OF STOCK PRODUCT
                if args["stock"] == str(0):
                    sse.publish({"message":f"Product {args['name'].upper()} from category {category.title.upper()} is out of stock."}, type="product")
                
                # SENDING NOTIFICATION TO USER ABOUT PRODUCT CAME BACK IN STOCK
                if old_stock == 0 and int(args["stock"]) > 0:
                    sse.publish({"message":f"Product {args['name'].upper()} from category {category.title.upper()} is back in stock."}, type="product")


                # DELETING THE OLD CACHE
                cache.delete("get_all_product")
                cache.delete_memoized(get_all_product_by_sm, str(product.created_by))
                return {"message":"Product updated successfully."}
        return {"message":"Not Allowed"}, 402
    
    @token_required
    def delete(self):
        if "role" in request.headers and "id" in request.args:
            role = request.headers["role"]
            product_id = request.args["id"]
            if role in  ["admin", "store_admin"]:
                product = Product.query.filter_by(id = product_id).first()
                sm_id = product.created_by
                if not product:
                    return {"message":"Category not found."}, 404
                db.session.delete(product)
                db.session.commit()

                # DELETING THE OLD CACHE
                cache.delete("get_all_product")
                cache.delete_memoized(get_all_product_by_sm, str(sm_id))

                return {"message":"Deleted successfully"}
        return {"message":"Not Allowed"}, 401
    


api.add_resource(ProductEndpoint, "/products")