from src import cache
from src.models import Category, CategoryChangeRequest, User, Product
from sqlalchemy import desc

#-----------------------FOR CATEGORY--------------------------------------
@cache.cached(timeout=86400, key_prefix="get_all_category")
def get_all_category():
    # cat = [i.output for i in models.Category.query.all()]
    cat = [{**i[0].output, **{"created_by_name": i.full_name}} for i in Category.query.join(User).add_columns(User.full_name).all()]
    return cat

@cache.memoize(86400)
def get_category_by_store_admin(user_id):
    cat = [i.output for i in Category.query.filter_by(created_by = user_id).all()]
    cat2 = [i.output for i in Category.query.filter_by(created_by = 4).all()]
    return cat + cat2
#-------------------------------------------------------------------------


#-----------------------FOR CATEGORY REQUEST------------------------------
@cache.cached(timeout=86400, key_prefix="get_all_requested_category")
def get_all_requested_category():
    cat = [{**i[0].output, **{"created_by_name": i.full_name}} for i in CategoryChangeRequest.query.join(User).add_columns(User.full_name).all()]
    return cat

@cache.memoize(86400)
def get_all_requested_category_by_store_admin(sm_id):
    cat = [{**i[0].output, **{"created_by_name": i.full_name}} for i in CategoryChangeRequest.query.join(User).add_columns(User.full_name).filter_by(id = sm_id).all()]
    return cat
#--------------------------------------------------------------------------


#-----------------------FOR PRODUCT----------------------------------------
@cache.cached(timeout=86400, key_prefix="get_all_product")
def get_all_product():
    products = [{**i[0].output, **{"category":i.title}} for i in Product.query.join(Category).add_columns(Category.title).order_by(desc(Category.title)).all()]
    products.reverse()
    return products

@cache.memoize(86400)
def get_all_product_by_sm(sm_id):
    products = [{**i[0].output, **{"category":i.title}} for i in Product.query.filter_by(created_by = sm_id).join(Category).add_columns(Category.title).order_by(desc(Category.title)).all()]
    products.reverse()
    return products
