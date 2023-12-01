from flask_restful import Resource
from src import api, tasks

class TestClass(Resource):
    def get(self):
        job = tasks.just_say_hello.delay("Manmay")
        return {"message":str(job)}

api.add_resource(TestClass, "/test")