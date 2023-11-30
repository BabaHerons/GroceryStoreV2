from src import api, db
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Category, CategoryChangeRequest
from src.utils import args

fields = ["title","description", "created_by", "created_by_name"]
category_args = args(fields)
category_patch_args = args(["category_id"] + fields)

request_fields = ["for_category", "request_type"] + fields
request_category_args = args(request_fields)
request_category_patch_args = args(request_fields + ["id", "status"])

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
    def put(self):
        args = category_patch_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role == "admin":
                args["is_active"] = True
                cat = Category.query.filter_by(id = args["category_id"]).first()
                for key, value in args.items():
                    if key in fields and value is not None:
                        if key not in ["created_by", "created_by_name"]:
                            setattr(cat, key, value)
                db.session.add(cat)
                db.session.commit()
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def patch(self):
        if "role" in request.headers and "id" in request.args:
            role = request.headers["role"]
            category_id = request.args["id"]
            if role == "admin":
                cat = Category.query.filter_by(id = category_id).first()
                if not cat:
                    return {"message":"Category not found."}, 404
                cat.is_active = True
                db.session.add(cat)
                db.session.commit()
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def delete(self):
        if "role" in request.headers and "id" in request.args:
            role = request.headers["role"]
            category_id = request.args["id"]
            if role == "admin":
                cat = Category.query.filter_by(id = category_id).first()
                if not cat:
                    return {"message":"Category not found."}, 404
                db.session.delete(cat)
                db.session.commit()
                return {"message":"Deleted successfully"}
        return {"message":"Not Allowed"}, 401


class CategoryRequestEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers and "user_id" in request.headers:
            role = request.headers["role"]
            user_id = request.headers["user_id"]
            if role == "admin":
                if "id" in request.args:
                    id = request.args["id"]
                    cat = CategoryChangeRequest.query.filter_by(id = id).first()
                    return cat.output
                categories = [i.output for i in CategoryChangeRequest.query.all()]
                return categories
            elif role == "store_admin":
                categories = [i.output for i in CategoryChangeRequest.query.filter_by(created_by=user_id).all()]
                return categories
            return {"message":"Not Allowed"}, 401
        return {"message":"Missing values in Headers."}, 400

    @token_required
    def post(self):
        args = request_category_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role =="store_admin":
                args["status"] = "pending"
                cat = CategoryChangeRequest(**args)
                db.session.add(cat)
                db.session.commit()

                cat = Category.query.filter_by(id = args["for_category"]).first()
                if not cat:
                    return {"message":"Category ID is missing."}
                cat.request_status = True
                db.session.add(cat)
                db.session.commit()
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def patch(self):
        args = request_category_patch_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role =="admin":
                cat = CategoryChangeRequest.query.filter_by(id = args["id"]).first()
                if not cat:
                    return {"message":"Request Category ID is missing."}
                cat.status = args["status"]
                db.session.add(cat)
                db.session.commit()
                
                cat = Category.query.filter_by(id = args["for_category"]).first()
                if not cat:
                    return {"message":"Category ID is missing."}
                cat.request_status = False
                if args["status"] == "approved":
                    cat.title = args["title"]
                    cat.description = args["description"]
                db.session.add(cat)
                db.session.commit()
                return {"message":"Action taken succesfully"}
        return {"message":"Not Allowed"}, 401



api.add_resource(CategoryEndpoint, "/category")
api.add_resource(CategoryRequestEndpoint, "/category-request")