from src import celery, mail
from flask import render_template
from datetime import datetime
from celery.schedules import crontab
from flask_mail import Message
from src.models import User, Order, OrderedItems, Product, Category
from src.utils import current_date_time

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

# celery.Task = ContextTask

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(5000, just_say_hello.s(), name="Runs every 5 seconds.")

@celery.task()
def just_say_hello():
    print("Inside Task")
    print(f"Hello, Manmay.")
    # return name

@celery.task()
def send_invoice_email(order_id):
    orders = [
        {**i[0].output, **{"user_full_name":i.full_name, "email":i.email}}
        for i in Order.query.filter_by(id=order_id)
        .join(User, User.id == Order.user_id)
        .add_columns(User.full_name, User.email)
        .all()
    ]
    for order in orders:
        products = [
            {**i[0].output, **{"name":i.name, "price":i.price, "unit":i.unit, "category":i.title}}
            for i in OrderedItems.query.filter_by(order_id  = order_id)
            .join(Product, Product.id == OrderedItems.product_id)
            .add_columns(Product.name, Product.price, Product.unit)
            .join(Category, Category.id == Product.category_id)
            .add_columns(Category.title)
            .all()
        ]
        order["products"] = products
    orders[0]["todays_date"] = current_date_time().strftime("%d-%m-%Y\n%H:%M:%S")

    msg = Message('User Sign Up Request', recipients=[orders[0]["email"]])
    msg.html = render_template('/invoice.html', order=orders[0])
    mail.send(msg)

    return "Mail Sent."