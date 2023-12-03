from src import cache, models

#-----------------------FOR CATEGORY--------------------------------------
@cache.cached(timeout=86400, key_prefix="get_all_category")
def get_all_category():
    cat = [i.output for i in models.Category.query.all()]
    return cat

@cache.memoize(86400)
def get_category_by_store_admin(user_id):
    cat = [i.output for i in models.Category.query.filter_by(created_by = user_id).all()]
    cat2 = [i.output for i in models.Category.query.filter_by(created_by = 4).all()]
    return cat + cat2
#-------------------------------------------------------------------------


#-----------------------FOR CATEGORY REQUEST------------------------------
@cache.cached(timeout=86400, key_prefix="get_all_requested_category")
def get_all_requested_category():
    cat = [i.output for i in models.CategoryChangeRequest.query.all()]
    return cat

@cache.memoize(86400)
def get_all_requested_category_by_store_admin(sm_id):
    cat = [i.output for i in models.CategoryChangeRequest.query.filter_by(created_by = sm_id).all()]
    return cat
#--------------------------------------------------------------------------