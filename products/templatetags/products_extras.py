from django import template

from products.models import *
from cart.models import * 

register = template.Library()


@register.simple_tag
def is_in_cart(pr_id, cart):
    items = cart.item_set.all()
    exist = items.filter(
        cart = cart,
        pr_id = pr_id,
    ).exists()
    return exist

@register.simple_tag
def is_in_favorite(pr_id, session_key):
    fav = Favorite.objects.get(
        session_key = session_key
    )
    items = fav.favoriteitem_set.all()
    exist = items.filter(
        favorite = fav,
        pr_id = pr_id,
    ).exists()
    return exist

@register.simple_tag 
def modify_imgsrc(imgsrc):
    imgsrc = imgsrc.url.replace('static/images/products/', '')
    imgsrc = imgsrc.replace('/static/images/products/', '')
    return imgsrc

@register.simple_tag
def sort_attributeitems(attr_items_set):
    sorted_result = attr_items_set.order_by('name')
    return sorted_result 

# @register.simple_tag
# def check_filter(products, filter_id):
#     print('it works')
    






