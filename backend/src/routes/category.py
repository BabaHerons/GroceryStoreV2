from src import api, db
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Category
from src.utils import args

fields = ["title","description", "created_by", "created_by_name"]
category_args = args(fields)
category_patch_args = args(["category_id"] + fields)

class CategoryEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers and "user_id" in request.headers:
            role = request.headers["role"]
            user_id = request.headers["user_id"]
            if role == "admin":
                if "id" in request.args:
                    id = request.args["id"]
                    cat = Category.query.filter_by(id = id).first()
                    return cat.output
                categories = [i.output for i in Category.query.all()]
                return categories
            elif role == "store_admin":
                categories = [i.output for i in Category.query.filter_by(created_by=user_id).all()]
                return categories
            return {"message":"Not Allowed"}, 401
        return {"message":"Missing values in Headers."}, 400
    
    @token_required
    def post(self):
        args = category_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["admin", "store_admin"]:
                if role == "admin":
                    args["is_active"] = True
                else:
                    args["is_active"] = False
                cat = Category(**args)
                db.session.add(cat)
                db.session.commit()
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def patch(self):
        args = category_patch_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role == "admin":
                args["is_active"] = True
                cat = Category.query.filter_by(id = args["category_id"]).first()
                for key, value in args.items():
                    if key in fields and value is not None:
                        setattr(cat, key, value)
                db.session.add(cat)
                db.session.commit()
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401


api.add_resource(CategoryEndpoint, "/category")