from src import api, SECRET_TOKEN_KEY, fernet, db
from flask_restful import Resource, reqparse
from src.jwt import token_required, create_token
from src.models import User
from src.utils import args, current_date_time
import jwt

login_args = args(["email", "password"])
token_args = args(["token"])

class Login(Resource):    
    def post(self):
        args = login_args.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if not user:
            return {"message": "User Not Found"}, 404
        
        user_password = args["password"]
        try:
            decoded_password = fernet.decrypt(user.password).decode()
        except:
            return {"message":"Invalid Fernet Token"}, 500
        if user_password == decoded_password:
            if user.is_active:
                token = create_token(user.id, user.role)
                
                # ADDING THE LAST LOGIN TIME OF THE USER
                user.last_login = current_date_time()
                db.session.add(user)
                db.session.commit()
                
                return {"token":token, "role":user.role, "full_name": user.full_name, "user_id":user.id}
            return {"message": "User Inactive. Please contact admin"}, 401
        return {"message": "Wrong Password"}, 401

class Verify_Token(Resource):
    @token_required
    def post(self):
        args = token_args.parse_args()
        data = jwt.decode(args['token'], SECRET_TOKEN_KEY, algorithms=['HS256'])
        user = User.query.filter_by(id=data['user']).first()
        return user.output


api.add_resource(Login, '/login')
api.add_resource(Verify_Token, '/verify_token')