from src import api, db, mail, fernet
from flask_restful import Resource
from flask import request
from flask_mail import Message
from src.jwt import token_required
from src.models import User
import random
from src.utils import args
from flask import render_template

otp_args = args(["otp", "email", "password"])
otp_request_args = args(["email"])
signUp_args = args(["full_name", "email", "password", "role"])
signUp_otp_args = args(["otp"])
activate_sm_args = args(["user_id","is_active"])

session_dict = {}

class UserEndpoint(Resource):
    @token_required
    def get(self):
        if "id" in request.args:
            user = User.query.filter_by(id = request.args['id']).first()
            if not user:
                return {"message": "User not found."}, 404
            return user.output
        elif "role" in request.headers:
            role = request.headers["role"]
            if role == "admin":
                Users = [i.output for i in User.query.all()]
                return Users
            return {"message":"Access Denied"}, 401
        return {"message":"Please provide user ID"}, 401

    @token_required
    def patch(self):
        if "role" in request.headers:
            role = request.headers["role"]
            if role == "admin":
                args = activate_sm_args.parse_args()
                user = User.query.filter_by(id = args['user_id']).first()
                if not user:
                    return {"message": "User not found."}, 404
                if args['is_active']:
                    user.is_active = True
                else:
                    user.is_active = False
                db.session.add(user)
                db.session.commit()
                return {"message":"Edit Successfull."}
        return {"message":"Access Denied"}, 401

class Sign_Up(Resource):
    def post(self):
        args = signUp_args.parse_args()
        if args["role"] in ["user", "store_admin"]:
            session_dict["sign_up_args"] = args
            if (args["role"] == "user"):
                session_dict["sign_up_args"]["is_active"] = True
            else:
                session_dict["sign_up_args"]["is_active"] = False
            otp = random.randint(111111, 999999)
            session_dict['sign_up_otp'] = otp

            # SENDING MAIL TO User FOR OTP
            try:
                msg = Message('User Sign Up Request', recipients=[args["email"]])
                msg.html = render_template('/signup_pass.html', admin=args, otp = otp)
                # msg.html = f"<h1>OTP: {otp}</h1>"
                mail.send(msg)
            except:
                return {"message": "Email send error"}, 500
            return {"message":"Email Sent", "otp": otp}
        return {"message":"Prohibitted Sign Up"}, 401

    def patch(self):
        args = signUp_otp_args.parse_args()
        if 'sign_up_otp' in session_dict:
            if (int(args['otp']) == session_dict['sign_up_otp']):
                del session_dict['sign_up_otp']
                session_dict["sign_up_args"]["password"] = fernet.encrypt(session_dict["sign_up_args"]["password"].encode())
                try:
                    user = User(**session_dict["sign_up_args"])
                    db.session.add(user)
                    db.session.commit()
                    del session_dict["sign_up_args"]
                except:
                    return {"message": "Please try again"}, 500
                return {"message": "User Sign Up Successfull."}
            else:
                del session_dict['sign_up_otp']
                return {"message": "Invalid OTP. Please Resend the OTP."}, 401
        return {"message": "Please Resend the OTP"}, 404


class Forgot_Password(Resource):
    def patch(self):
        args = otp_args.parse_args()
        if 'otp' in session_dict:
            if (int(args['otp']) == session_dict['otp']):
                del session_dict['otp']

                user = User.query.filter_by(email = args['email']).first()
                if not user:
                    return {"message": "Email not found."}, 404
                
                user.password = fernet.encrypt(args['password'].encode())
                db.session.add(user)
                db.session.commit()

                return {"message": "Password Reset Successfull."}
            return {"message": "Invalid OTP"}, 401
        return {"message": "Please Resend the OTP"}, 404

    def post(self):
        try:
            args = otp_request_args.parse_args()
        except:
            return {"message": "Please provide email."}, 404
        
        user = User.query.filter_by(email = args['email']).first()
        if not user:
            return {"message": "Email not found."}, 404
        
        otp = random.randint(111111,999999)
        session_dict['otp'] = otp
        print(session_dict['otp'])

        # user email
        msg = Message('Password Reset Request', recipients=[user.email])
        msg.html = render_template('/forgot_pass.html', admin = user.output, otp = otp)
        mail.send(msg)

        return {"message" : "Mail sent."}

    


api.add_resource(UserEndpoint, '/users')
api.add_resource(Forgot_Password, '/forgot-password')
api.add_resource(Sign_Up, '/sign-up')