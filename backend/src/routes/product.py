from src import api, db, cache
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Product
from src.utils import args, current_date_time_to_id
from flask_sse import sse
from src.custom_cache import get_all_product

fields = ["name", "description", "category", "category_id", "image", "m_date", "e_date",
          "stock", "price", "created_by"]
product_post_args = args(fields)
product_put_args = args(fields + ["id"])

class ProductEndpoint(Resource):
    @token_required
    def get(self):
        if "id" in request.args:
            product_id = request.args["id"]
            product = Product.query.filter_by(id=product_id).first()
            return product.output
        products = get_all_product()
        return products

    @token_required
    def post(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["store_admin","admin"]:
                args = product_post_args.parse_args()
                args["id"] = f"PROD{current_date_time_to_id()}"
                product = Product(**args)
                db.session.add(product)
                db.session.commit()

                # SENDING NOTIFICATION TO USER ABOUT NEW ADDITION OF PRODUCT
                sse.publish({"message":f"New product {args['name']} has been added to category {args['category']}"}, type="product")
                
                # DELETING THE OLD CACHE
                cache.delete("get_all_product")
                return {"message":"Product added successfully."}
        return {"message":"Not Allowed"}, 402
    
    @token_required
    def put(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["store_admin","admin"]:
                args = product_put_args.parse_args()
                product = Product.query.filter_by(id=args["id"]).first()
                if not product:
                    return {"message":"No products found."}, 404
                if str(product.created_by) == str(args["created_by"]):
                    for key, value in args.items():
                        if key in fields and value is not None:
                            if key != "created_by":
                                setattr(product, key, value)
                    db.session.add(product)
                    db.session.commit()

                # DELETING THE OLD CACHE
                cache.delete("get_all_product")
                return {"message":"Product added successfully."}
        return {"message":"Not Allowed"}, 402
    
    @token_required
    def delete(self):
        if "role" in request.headers and "id" in request.args:
            role = request.headers["role"]
            product_id = request.args["id"]
            if role in  ["admin", "store_admin"]:
                product = Product.query.filter_by(id = product_id).first()
                if not product:
                    return {"message":"Category not found."}, 404
                db.session.delete(product)
                db.session.commit()

                # DELETING THE OLD CACHE
                cache.delete("get_all_product")
                return {"message":"Deleted successfully"}
        return {"message":"Not Allowed"}, 401
    


api.add_resource(ProductEndpoint, "/products")