from src import api
from flask_restful import Resource, reqparse
from src.jwt import token_required, create_token, secret_token_key
from src.models import User
from src.utils import args
import jwt

login_args = args(["email", "password"])
token_args = args(["token"])

class Login(Resource):    
    def post(self):
        args = login_args.parse_args()
        user = User.query.filter_by(email=args['email'], password = args['password']).first()
        if not user:
            return {"message": "Email or Password is wrong."}, 401
        token = create_token(user.id)
        return {"token":token, "role":user.role}

class Verify_Token(Resource):
    @token_required
    def post(self):
        args = token_args.parse_args()
        data = jwt.decode(args['token'], secret_token_key, algorithms=['HS256'])
        user = User.query.filter_by(id=data['user']).first()
        return user.output


api.add_resource(Login, '/login')
api.add_resource(Verify_Token, '/verify_token')