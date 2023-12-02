from src import cache, models

@cache.cached(timeout=86400, key_prefix="all_category")
def get_all_category():
    cat = [i.output for i in models.Category.query.all()]
    return cat

@cache.memoize(86400)
def get_category_by_store_admin(user_id):
    cat = [i.output for i in models.Category.query.filter_by(created_by = user_id).all()]
    return cat
