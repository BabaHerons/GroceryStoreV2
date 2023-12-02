from flask_restful import Resource
from src import api, tasks, cache
from flask_sse import sse
from src.custom_cache import get_category_by_store_admin

class TestClass(Resource):
    def get(self):
        job = tasks.just_say_hello.delay()
        return {"message":str(job)}

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