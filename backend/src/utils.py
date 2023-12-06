import datetime
from pytz import timezone
from flask import request
from flask_restful import reqparse
# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

def current_date_time():
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    return now

def current_date_time_to_id():
    now = datetime.datetime.now(timezone('Asia/Kolkata'))
    return now.strftime("%Y%m%d%H%M%S%f")

def entries():
    if 'entries' in request.args:
        try:
            number = int(request.args['entries'])
        except:
            return 10
    else:
        number = 10
    return number

def offset():
    if 'offset' in request.args:
        try:
            number = int(request.args['offset'])
        except:
            return 0
    else:
        number = 0
    return number

def args(l:list, required=True):
    arguments = reqparse.RequestParser()
    for i in l:
        arguments.add_argument(i, help = f"Please provide {i}", required=required)
    return arguments