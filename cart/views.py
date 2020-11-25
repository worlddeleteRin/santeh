from django.shortcuts import render

from django.shortcuts import render
from .models import * 
from django.http import JsonResponse, HttpResponse
import urllib
import os
from django.core.files.storage import default_storage
from santeh.settings import * 
from products.models import * 



def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def get_or_create_cart(request):
    session_key = get_session_key(request)
    current_cart = Cart.objects.get_or_create(
        session_key = session_key,
    )[0],
    return current_cart[0]

def get_or_create_favorite(request):
    session_key = get_session_key(request)
    current_favorite = Favorite.objects.get_or_create(
        session_key = session_key
    )[0]
    return current_favorite


def index(request):
    session_key = get_session_key(request)
    fav = get_or_create_favorite(request)
    session_key = get_session_key(request)
    cart = get_or_create_cart(request)

    categories = Category.objects.all()
    return render(request, 'cart/index.html', {
        'categories': categories,
        'cart': cart,
        'fav_main': fav,
        'session_key': session_key,
    })

def offer(request):
    session_key = get_session_key(request)
    cart = get_or_create_cart(request)

    categories = Category.objects.all()
    return render(request, 'cart/offer.html', {
        'categories': categories,
        'cart': cart,
    })

def order_created(request):
    session_key = get_session_key(request)

    categories = Category.objects.all()
    return render(request, 'cart/order_created.html', {
        'categories': categories,
    })


def add_item_ajax(request):
    cart = get_or_create_cart(request)
    is_new = 'yes'
    pr_id = request.GET['product_id']
    pr = Product.objects.get(
        id = pr_id,
    )
    if (Item.objects.filter(
        cart = cart,
        pr_id = pr.id,
    ).exists()):
        item = Item.objects.get(
           cart = cart,
            pr_id = pr.id, 
        )
        item.delete()
        in_cart = 'no'
        # item = Item.objects.get(
        #    cart = cart,
        #     pr_id = pr.id, 
        # )
        # item.quantity += 1
        # item.save()
    else:
        item = Item(
            cart = cart,
            pr_id = pr.id,
            name = pr.name,
            price = pr.price,
            sale_price = pr.sale_price,
            imgsrc = pr.imgsrc,
        )
        item.save()
        in_cart = 'yes'
    
    return JsonResponse({
        'is_new': is_new,
        'in_cart': in_cart,
    }, status = 200 )

def delete_from_cart_ajax(request):
    cart = get_or_create_cart(request)
    item_id = request.GET['item_id']
    item = Item.objects.get(
        cart = cart,
        id = item_id
    )
    cart.item_set.remove(item)
    return JsonResponse({
        'deleted': 'yes'
    }, status = 200)

def update_cart_info_ajax(request):
    cart = get_or_create_cart(request)
    cart_total = cart.get_total()
    cart_quantity = cart.item_set.count()
    return JsonResponse({
        'cart_total': cart_total,
        'cart_quantity': cart_quantity,
        'deleted': 'yes'
    }, status = 200)

def remove_quantity_ajax(request):
    cart = get_or_create_cart(request)
    item_id = request.GET['item_id']
    item = Item.objects.get(
        cart = cart,
        id = item_id,
    )
    if item.quantity == 1:
        item.delete()
        is_removed = 'yes'
        return JsonResponse({
        'is_removed': is_removed,
    }, status = 200)
    else:
        item.quantity -= 1
        item.save()
        is_removed = 'no'
        if (item.has_sale()):
            has_sale = 'yes'
            pr_price = item.product_price()
            pr_sale = item.product_sale_price()
            discount_val = item.discount_val()
            return JsonResponse({
            'has_sale': has_sale,
            'is_removed': is_removed,
            'item_price': pr_price,
            'item_sale': pr_sale,
            'item_discount_val': discount_val,
            'item_quantity': item.quantity,
        }, status = 200)
        else:
            has_sale = 'no'
            pr_price = item.product_price()
            return JsonResponse({
            'has_sale': has_sale,
            'is_removed': is_removed,
            'item_price': pr_price,
            'item_quantity': item.quantity,
        }, status = 200)

        
    

def add_quantity_ajax(request):
    print('request is here')
    cart = get_or_create_cart(request)
    try:
        request.GET['from_prpage']
        item_id = request.GET['item_id']
        item = Item.objects.get(
            cart = cart,
            pr_id = item_id,
        )
    except:
        item_id = request.GET['item_id']
        item = Item.objects.get(
        cart = cart,
        id = item_id,
        )

    
    
    
    item.quantity += 1
    item.save()

    if item.has_sale():
        has_sale = 'yes'
        pr_price = item.product_price()
        pr_sale = item.product_sale_price()
        discount_val = item.discount_val()
        return JsonResponse({
            'has_sale': has_sale,
            'item_price': pr_price,
            'item_sale': pr_sale,
            'item_discount_val': discount_val,
            'item_quantity': item.quantity,
        }, status = 200)
    else:
        has_sale = 'no'
        pr_price = item.product_price()
        return JsonResponse({
        'has_sale': has_sale,
        'item_price': pr_price,
        'item_quantity': item.quantity,
    }, status = 200)

def check_in_cart_ajax(request):
    cart = get_or_create_cart(request)
    item_id = request.GET['product_id']
    in_cart = ''
    if (Item.objects.filter(
        cart = cart,
        pr_id = item_id).exists()):
        in_cart = 'yes'
        current_item = Item.objects.get(
            cart = cart,
            pr_id = item_id
        )
        return JsonResponse({
            'in_cart': in_cart,
            'quantity': current_item.quantity,
        }, status = 200)
    else:
        in_cart = 'no'
        return JsonResponse({
            'in_cart': in_cart,
        }, status = 200)

def favorite(request):
    session_key = get_session_key(request)
    current_fav = get_or_create_favorite(request)
    fav_items = current_fav.favoriteitem_set.all()
    fav_items = fav_items.values_list('pr_id')
    fav_items = Product.objects.filter(
        id__in = fav_items
    )
    cart = get_or_create_cart(request)
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'cart/favorite.html', {
        'categories': categories,
        # 'products': fav_items,
        'session_key': session_key,
        'fav_main': current_fav,
        'cart': cart,
        'fav_items': fav_items,
    })


def favorite_add_or_delete_ajax(request):
    pr_id = request.GET['product_id']
    exist = ''
    fav = get_or_create_favorite(request)
    fav_items = fav.favoriteitem_set.all()
    if (fav_items.filter(
        pr_id = pr_id,
    ).exists()):
        curr_item = fav_items.get(pr_id = pr_id)
        print(curr_item)
        curr_item = Favoriteitem.objects.get(id = curr_item.id)
        curr_item.delete()

        exist = 'deleted'
        return JsonResponse({
            'exist': exist,
        }, status = 200)
    else:
        item = Favoriteitem(
            favorite = fav,
            pr_id = pr_id
        )
        item.save()
        exist = 'added'
        return JsonResponse({
            'exist': exist,
        }, status = 200)

def update_cart_total_ajax(request):
    cart = get_or_create_cart(request)
    cart_total = cart.items_in_cart()
    return JsonResponse({
        'cart_total': cart_total,
    }, status = 200)

def update_fav_total_ajax(request):
    fav = get_or_create_favorite(request)
    fav_total = fav.get_items()
    return JsonResponse({
        'fav_total': fav_total,
    }, status = 200)

