from src import api, db, cache
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Category, CategoryChangeRequest, User
from src.utils import args
from flask_sse import sse
from time import perf_counter_ns
from src.custom_cache import get_all_category, get_category_by_store_admin, get_all_requested_category, get_all_requested_category_by_store_admin

fields = ["title","description", "created_by"]
category_args = args(fields)
category_patch_args = args(["category_id"] + fields)

request_fields = ["for_category", "request_type"] + fields
request_category_args = args(request_fields)
request_category_patch_args = args(request_fields + ["id", "status"])

delete_request_category_args = args(["id", "status", "for_category"])

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
                categories = get_all_category()
                return categories
            elif role == "store_admin":
                # start = perf_counter_ns()
                categories = get_category_by_store_admin(user_id)
                # stop = perf_counter_ns()
                # print()
                # print(stop - start)
                # print()
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

                sm = User.query.filter_by(id = args["created_by"]).first()
                # SENDING NOTIFICATION TO ADMIN ABOUT NEW CATEGORY CREATION
                if role == "store_admin":
                    sse.publish({"message":f"Store admin {sm.full_name} requested to create a category {args['title']}"}, type="cat_req")
                
                # DELETING THE OLD CACHE
                cache.delete("get_all_category")
                if role == "store_admin":
                    cache.delete_memoized(get_category_by_store_admin, args["created_by"])
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
                if not cat:
                    return {"message":"Category not found."}, 404
                title = cat.title.upper()
                for key, value in args.items():
                    if key in fields and value is not None:
                        if key != "created_by":
                            setattr(cat, key, value)
                db.session.add(cat)
                db.session.commit()

                user = User.query.filter_by(id = cat.created_by).first()
                 # PUBLISH TO THE STORE ADMIN FOR THE ACTIVATION OF CATEGORY SHE/HE CREATED
                sse.publish({"message":f"Admin has UPDATED the category {title} with ID: {cat.id}"}, type=f"{cat.created_by}-{user.full_name}")

                # DELETING THE OLD CACHE
                cache.delete("get_all_category")
                cache.delete_memoized(get_category_by_store_admin, str(cat.created_by))
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

                user = User.query.filter_by(id = cat.created_by).first()
                # PUBLISH TO THE STORE ADMIN FOR THE ACTIVATION OF CATEGORY SHE/HE CREATED
                sse.publish({"message":f"Admin has APPROVED the category {cat.title.upper()}"}, type=f"{cat.created_by}-{user.full_name}")

                # DELETING THE OLD CACHE
                cache.delete("get_all_category")
                cache.delete_memoized(get_category_by_store_admin, str(cat.created_by))
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
                sm_id = cat.created_by
                title = cat.title.upper()
                db.session.delete(cat)
                db.session.commit()

                user = User.query.filter_by(id = sm_id).first()
                # PUBLISH TO THE STORE ADMIN FOR THE ACTIVATION OF CATEGORY SHE/HE CREATED
                sse.publish({"message":f"Admin has DELETED the category {title}"}, type=f"{sm_id}-{user.full_name}")

                # DELETING THE OLD CACHE
                cache.delete("get_all_category")
                cache.delete_memoized(get_category_by_store_admin, str(cat.created_by))
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
                categories = get_all_requested_category()
                return categories
            elif role == "store_admin":
                categories = get_all_requested_category_by_store_admin(user_id)
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

                sm = User.query.filter_by(id = cat.created_by).first()
                # SERVER SIDE EVENTS
                # (FOR SENDING PUSH NOTIFICATION TO THE ADMIN ABOUT NEW REUEST)
                req_type = args["request_type"]
                sse.publish({"message":f"Store Admin: {sm.full_name} has requested {req_type.upper()} for {cat.title}."}, type="cat_req")

                # REMOVE THE CACHING
                cache.delete("get_all_category")
                cache.delete("get_all_requested_category")
                cache.delete_memoized(get_category_by_store_admin, args["created_by"])
                cache.delete_memoized(get_all_requested_category_by_store_admin, args["created_by"])

                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def patch(self):
        args = request_category_patch_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role =="admin":
                cat_req = CategoryChangeRequest.query.filter_by(id = args["id"]).first()
                if not cat_req:
                    return {"message":"Request Category ID is missing."}
                cat_req.status = args["status"]
                db.session.add(cat_req)
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

                sm = User.query.filter_by(id = cat_req.created_by).first()
                # SERVER SIDE EVENTS
                # (FOR SENDING PUSH NOTIFICATION TO THE STORE ADMIN ABOUT ADMIN RESPONSE)
                req_status = args["status"]
                sse.publish({"message":f"Admin has {req_status.upper()} your EDIT request for {cat.title.upper()} with ID: {cat.id}."}, type=f"{sm.id}-{sm.full_name}")

                # REMOVE THE CACHING
                cache.delete("get_all_category")
                cache.delete("get_all_requested_category")
                cache.delete_memoized(get_category_by_store_admin, args["created_by"])
                cache.delete_memoized(get_all_requested_category_by_store_admin, args["created_by"])

                return {"message":"Action taken succesfully"}
        return {"message":"Not Allowed"}, 401
    
    @token_required
    def delete(self):
        args = delete_request_category_args.parse_args()
        if "role" in request.headers:
            role = request.headers["role"]
            if role =="admin":
                cat_req = CategoryChangeRequest.query.filter_by(id = args["id"]).first()
                if not cat_req:
                    return {"message":"Request Category ID is missing."}
                cat_req.status = args["status"]
                db.session.add(cat_req)
                db.session.commit()
                
                cat = Category.query.filter_by(id = args["for_category"]).first()
                if not cat:
                    return {"message":"Category ID is missing."}
                if args["status"] == "approved":
                    db.session.delete(cat)
                    db.session.commit()
                else:
                    cat.request_status = False
                    db.session.add(cat)
                    db.session.commit()

                sm = User.query.filter_by(id = cat_req.created_by).first()
                # SERVER SIDE EVENTS
                # (FOR SENDING PUSH NOTIFICATION TO THE STORE ADMIN ABOUT ADMIN RESPONSE)
                req_status = args["status"]
                sse.publish({"message":f"Admin has {req_status.upper()} your DELETE request for {cat_req.title}."}, type=f"{sm.id}-{sm.full_name}")

                # REMOVE THE CACHING
                cache.delete("get_all_category")
                cache.delete("get_all_requested_category")
                cache.delete_memoized(get_category_by_store_admin, str(sm.id))
                cache.delete_memoized(get_all_requested_category_by_store_admin, str(sm.id))

                return {"message":"Deleted succesfully"}
        return {"message":"Not Allowed"}, 401


api.add_resource(CategoryEndpoint, "/category")
api.add_resource(CategoryRequestEndpoint, "/category-request")