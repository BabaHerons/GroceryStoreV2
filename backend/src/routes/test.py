from flask_restful import Resource
from src import api, tasks
from flask_sse import sse

class TestClass(Resource):
    def get(self):
        job = tasks.just_say_hello.delay()
        return {"message":str(job)}

class SSEtesting(Resource):
    def get(self):
        sse.publish({"message":"Hello, from Groccery Store APP."}, type="greeting")
        return {"message":"Message sent successfully."}

api.add_resource(TestClass, "/test")
api.add_resource(SSEtesting, "/sse")