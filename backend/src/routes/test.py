from flask_restful import Resource
from src import api, tasks, cache
from flask_sse import sse
from src.custom_cache import get_category_by_store_admin
from flask import send_file
from io import BytesIO
import os

class TestClass(Resource):
    def get(self):
        # job = tasks.just_say_hello.delay()
        job = tasks.export_products_csv.s().apply_async()
        result= job.wait()
        filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../exports/products.csv")
        return send_file(filepath, mimetype='text/csv')
        # return {"message":str(result)}

class SSEtesting(Resource):
    def get(self):
        sse.publish({"message":"Hello, from Groccery Store APP."}, type="greeting")
        return {"message":"Message sent successfully."}

class DeleteCache(Resource):
    def get(self):
        cache.delete_memoized(get_category_by_store_admin, "10")
        return {"message": "Cache Deleted Successfully"}

api.add_resource(TestClass, "/test")
api.add_resource(SSEtesting, "/sse")
api.add_resource(DeleteCache, "/cache")