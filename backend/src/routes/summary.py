from src import api
from flask_restful import Resource
from flask import request, send_file
from src.jwt import token_required
import os


class ProductsReportEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["admin", "store_admin"]:
                filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../sales_report/products.png")
                return send_file(filepath, mimetype='image/png')
        return {"message":"Not Allowed"}, 401

class CategoryReportEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role in ["admin", "store_admin"]:
                filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../sales_report/category.png")
                return send_file(filepath, mimetype='image/png')
        return {"message":"Not Allowed"}, 401


api.add_resource(ProductsReportEndpoint, "/monthly-sales-report/products")
api.add_resource(CategoryReportEndpoint, "/monthly-sales-report/category")