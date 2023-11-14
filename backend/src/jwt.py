import jwt
from src import SECRET_TOKEN_KEY
from functools import wraps
from datetime import datetime, timedelta
from flask import request

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' in request.headers:
            token = request.headers['token']
        else:
            return {"message":"Not Authorised."}, 401
        
        try:
            data = jwt.decode(token, SECRET_TOKEN_KEY, algorithms=['HS256'])
        except :
            return {"message":"Invalid TOKEN."}, 401
        return f(*args, **kwargs)
    return decorated


def create_token(id):
    token = jwt.encode({
            "user": id,
            "exp": datetime.utcnow() + timedelta(minutes=120)
            }, SECRET_TOKEN_KEY)
    return token