from src import api, db, cache
from flask_restful import Resource
from flask import request
from src.jwt import token_required
from src.models import Order, OrderedItems, Product, Category, Cart
from src.utils import args, current_date_time, current_date_time_to_id
from src.custom_cache import get_all_order, get_all_product_by_sm
import json

fields = ["products", "amount"]
order_args = args(fields)

class OrderEndpoint(Resource):
    @token_required
    def get(self):
        if "role" in request.headers and "user_id" in request.headers:
            role = request.headers["role"]
            user_id = request.headers["user_id"]
            if role == "user":
                cart = [
                    {
                        **i[0].output, 
                        **{
                            "name":i.name, 
                            "price":i.price, 
                            "unit":i.unit,
                            "date":i.date,
                            "amount":i.amount,
                            "title":i.title,
                        }
                    }
                    for i in OrderedItems.query.filter_by(user_id = user_id)
                    .join(Product, OrderedItems.product_id == Product.id)
                    .add_columns(Product.name, Product.price, Product.unit)
                    .join(Order, Order.id == OrderedItems.order_id)
                    .add_columns(Order.date, Order.amount)
                    .join(Category, Category.id == Product.category_id)
                    .add_columns(Category.title)
                    .all()
                ]
                return cart
            if role == "admin":
                orders = get_all_order()
                return orders
            return {"message":"Not Allowed"}, 401
        return {"message":"Missing values in Headers."}, 400

    @token_required
    def post(self):
        args = order_args.parse_args()
        products = json.loads(args["products"])
        if "role" in request.headers and "user_id" in request.headers:
            role = request.headers["role"]
            user_id = request.headers["user_id"]
            if role == "user":
                date = current_date_time()
                order_id = current_date_time_to_id()
                order = Order(
                    id=order_id,
                    user_id=user_id,
                    date=date,
                    amount=args["amount"],
                    status="confirm"
                )
                db.session.add(order)
                db.session.commit()

                for item in products:
                    # CHECKING THE STOCK QUANTITY
                    product = Product.query.filter_by(id = item["product_id"]).first()
                    if product:
                        if float(product.stock) > float(item["quantity"]):
                            ordered_item = OrderedItems(
                                order_id=order_id,
                                product_id=item["product_id"],
                                quantity=item["quantity"],
                                item_total=item["item_total"],
                                user_id=user_id
                            )
                            db.session.add(ordered_item)
                            db.session.commit()

                            # REDUCING THE PRODUCT STOCK
                            product.stock = float(product.stock) - float(item["quantity"])
                            db.session.add(product)
                            db.session.commit()

                            # DELETING EVERY PRODUCT FROM CART
                            cart = Cart.query.filter_by(id = item["id"]).first()
                            if cart:
                                db.session.delete(cart)
                                db.session.commit()
                
                # DELETING THE CACHE
                cache.delete("get_all_order")
                cache.delete("get_all_product")
                cache.delete_memoized(get_all_product_by_sm, str(product.created_by))
                return {"message":"Added successfully"}
        return {"message":"Not Allowed"}, 401

api.add_resource(OrderEndpoint, "/orders")