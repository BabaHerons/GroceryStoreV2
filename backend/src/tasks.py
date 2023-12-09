from src import celery, mail, app
from flask import render_template
from celery.schedules import crontab
from flask_mail import Message
from src.models import User, Order, OrderedItems, Product, Category, Cart
from src.utils import current_date_time
from src.custom_cache import get_all_product, get_all_product_by_sm, get_all_order
import pandas as pd
import matplotlib.pyplot as plt
import os


# -------------------------------------------------------------
# CELERY WORKER (BATCH JOBS)
# celery -A main.celery worker -l info
# -------------------------------------------------------------
# CELERY BEAT (SCHEDULED JOBS)
# celery -A main.celery beat --max-interval 1 -l info
# -------------------------------------------------------------


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    # sender.add_periodic_task(5000, just_say_hello.s(), name="Runs every 5 seconds.")

    # REMINDING USER DAILY AT 7:00 PM
    sender.add_periodic_task(crontab(hour=19, minute=0), reminding_user.s())

    # MONTHLY REPORT TO BE SENT 1ST OF EVERY MONTH
    sender.add_periodic_task(crontab(day_of_month=1), send_sales_report.s())

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
    users = [i.output for i in User.query.filter_by(role="user").all()]
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

# ASYNC JOB FOR REPORTING SALES
@celery.task()
def sales_report():
    orders = get_all_order()
    product_report = {}
    category_report = {}
    for order in orders:
        for item in order["products"]:
            if item['name'] not in product_report:
                product_report[item["name"]] = 0
            product_report[item["name"]] += item["quantity"]

            if item["category"] not in category_report:
                category_report[item["category"]] = 0
            category_report[item["category"]] += item["quantity"]
    
    fig, ax = plt.subplots(1, figsize = (15, 8))
    fig.autofmt_xdate()
    plt.bar(range(len(product_report)), list(product_report.values()))
    plt.xticks(range(len(product_report)), list(product_report.keys()))
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sales_report/products.png")
    plt.savefig(filepath)

    plt.clf()

    fig, ax = plt.subplots(1, figsize = (10, 8))
    fig.autofmt_xdate()
    plt.bar(range(len(category_report)), list(category_report.values()))
    plt.xticks(range(len(category_report)), list(category_report.keys()))
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sales_report/category.png")
    plt.savefig(filepath)

    return "Completed"
            
@celery.task()
def send_sales_report():
    users = [i.output for i in User.query.filter_by(role = "admin").all()] + [i.output for i in User.query.filter_by(role = "store_admin").all()]
    job = sales_report.delay()

    filepath_product = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sales_report/products.png")
    filepath_category = os.path.join(os.path.abspath(os.path.dirname(__file__)), "sales_report/category.png")
    for user in users:
        user["todays_date"] = current_date_time().strftime("%B %d, %Y")
        user["todays_time"] = current_date_time().strftime("%I:%M:%S %p")
        msg = Message(f"Monthly Sales Report - {current_date_time().strftime('%B')}", recipients=[user["email"]])

        # ADDING THE ATTACHMENTS
        with app.open_resource(filepath_product) as fp:
            msg.attach("products_sales_report.png", "image/png", fp.read())
        with app.open_resource(filepath_category) as fp:
            msg.attach("category_sales_report.png", "image/png", fp.read())
        
        # CREATING THE EMAIL BODY
        msg.html = render_template('/monthly_report.html', user=user)

        # SENDING THE MAIL
        try:
            mail.send(msg)
        except:
            continue
    return "Monthly report sent."

