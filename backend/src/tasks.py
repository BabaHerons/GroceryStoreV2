from src import celery, mail, app
from flask import render_template
from datetime import datetime
from celery.schedules import crontab
from flask_mail import Message
from src.models import User, Order, OrderedItems, Product, Category, Cart
from src.utils import current_date_time
from src.custom_cache import get_all_product, get_all_product_by_sm
import pandas as pd
import os

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    # sender.add_periodic_task(5000, just_say_hello.s(), name="Runs every 5 seconds.")

    # REMINDING USER DAILY AT 7:00 PM
    sender.add_periodic_task(crontab(hour=19, minute=52), reminding_user.s())

@celery.task()
def just_say_hello():
    print("Inside Task")
    print(f"Hello, Manmay.")
    # return name

# ASYNC JOB FOR SENDING INVOICE
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
    orders[0]["todays_date"] = current_date_time().strftime("%B %d, %Y")
    orders[0]["todays_time"] = current_date_time().strftime("%I:%M:%S %p")

    msg = Message(f'Invoice for Order ID:{orders[0]["id"]}', recipients=[orders[0]["email"]])
    msg.html = render_template('/invoice.html', order=orders[0])
    mail.send(msg)

    return "Mail Sent."

# ASYNC JOB FOR EXPORTING THE PRODUCTS INTO CSV FILE
@celery.task()
def export_products_csv(sm_id = None):
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "exports/products.csv")
    if sm_id == None:
        products = get_all_product()
    else:
        products = get_all_product_by_sm(sm_id)
    df = pd.DataFrame(products)
    df.to_csv(rf"{filepath}", index=False)
    # print(df)
    # print(filepath)
    return "Saved"

# ASYNC JOB FOR REMINDING USER TO COME BACK
@celery.task()
def reminding_user():
    users = [i.output for i in User.query.all()]
    for user in users:
        user["todays_date"] = current_date_time().strftime("%B %d, %Y")
        user["todays_time"] = current_date_time().strftime("%I:%M:%S %p")
        cart = [
            {**i[0].output, **{"name":i.name, "price":i.price, "unit":i.unit, "category":i.title}}
            for i in Cart.query.filter_by(user_id = user["id"])
            .join(Product, Cart.product_id == Product.id)
            .add_columns(Product.name, Product.price, Product.unit)
            .join(Category, Product.category_id == Category.id)
            .add_columns(Category.title)
            .all()
        ]
        if len(cart) == 0:
            # REMIND USER TO VISIT AGAIN
            msg = Message(f'Long time no see.', recipients=[user["email"]])
            msg.html = render_template('/reminder.html', user=user)
        else:
            # REMIND USER THAT ITEM IS STILL IN THE CART
            user["grand_total"] = 0
            for item in cart:
                item_total = float(item["quantity"]) * float(item["price"])
                user["grand_total"] += item_total
                item["item_total"] = item_total
            msg = Message(f'Your items are waiting in the cart.', recipients=[user["email"]])
            msg.html = render_template('/reminder_cart.html', user=user, cart=cart)

        # SENDING MAIL TO THE USER
        try:
            mail.send(msg)
        except:
            continue
    return "Job Done."

    
