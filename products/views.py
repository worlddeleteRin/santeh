
from django.shortcuts import render
from .models import * 
from django.http import JsonResponse, HttpResponse
import urllib
import os
from django.core.files.storage import default_storage
from santeh.settings import * 
from cart.models import * 
import json
from django.template.loader import render_to_string



# Create your views here.

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

def get_not_active_filters():
    return ['Артикул производителя:', 
            'Комплектация:']

def index(request):
    fav = get_or_create_favorite(request)
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    categories = Category.objects.all()
    # destinations = Destination.objects.all()
    products = Product.objects.all()
    stock_products = products.filter(
        sale_price__gte = 1
    )
    stock_products = stock_products[:30]
    products = products[:50]

    template = 'products/index.html'
    page_template='products/blocks/products_list.html'

    context = {
        'fav_main': fav,
        'categories': categories,
        'products': products,
        'stock_products': stock_products,
        'session_key': session_key,
        'cart': cart,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

def product(request, product_id):
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    fav = get_or_create_favorite(request)
    current_product = Product.objects.get(id = product_id)
    categories = Category.objects.all()
    return render(request, 'products/product.html', {
        'product': current_product,
        'fav_main': fav,
        'cart': cart,
        'session_key': session_key,
        'categories': categories,
    })



def destination(request, cat_id, dest_id):
    session_key = get_session_key(request)
    current_cat = Category.objects.get(
        id = cat_id,
    )
    current_dest = Destination.objects.get(
        category = current_cat,
        id = dest_id,
    )
    products = current_dest.product_set.all()
    return render(request, 'products/dest.html', {
        'current_cat': current_cat,
        # 'current_dest': current_dest,
        'products': products,
    })

def on_sale(request):
    categories = Category.objects.all()
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    fav = get_or_create_favorite(request)
    products = Product.objects.filter(
        sale_price__gte = 1
    )
    context = {
        'fav_main': fav,
        'cart': cart,
        'categories': categories,
        'session_key': session_key,
        'products': products,
    }
    template = 'products/on_sale.html'
    page_template='products/blocks/products_list.html'
    if request.is_ajax():
        template = page_template
    return render(request, template, context )

def category(request, cat_id):
    print('start category view')
    not_active_filters = get_not_active_filters()
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    fav = get_or_create_favorite(request)
    print('cart, session_key, fav got')
    categories = Category.objects.all()
    
    current_cat = Category.objects.get(
        id = cat_id,
    )
    print('current category got')
    
    products = current_cat.product_set.all()
    # products = products[:100]
    print('products length is:', len(products))
    print('products got')

    template='products/category.html'
    page_template='products/blocks/products_list.html'

    context = {
        'page_template': page_template,
        'current_cat': current_cat,
        # 'current_dest': current_dest,
        'products': products,
        'fav_main': fav,
        'cart': cart,
        'session_key': session_key,
        'current_cat': current_cat,
        'not_active_filters': not_active_filters,
        'categories': categories,
        # 'active_filter_items': active_filter_items,
    }
    if request.is_ajax():
        print('that was an ajax request')
        template = page_template

    try:
        filters = request.GET['filters']
        print('filters is', filters)
        active_filter_items = []
        if filters:
            if len(filters) > 0:
                filters = filters.split('_')   
                # attr_list = []
                # attr_items_list = []
                # active_filter_items = []
                for f_item in filters:
                    f_item = f_item.split('-')
                    attr_id = f_item[0]
                    f_item.pop(0)
                    products = products.filter(
                        attributeitem__id__in = f_item
                    )
            context['products'] = products
            return render(request, template,
    context)
            # return JsonResponse({
            #     'result': True,
            #     'products': render_to_string(
            #         request = request,
            #         template_name = template,
            #         context = context
            #     )
            # })
    except:
        pass

    print('current template is: ', template)
    return render(request, template,
    context)

def filter_products_ajax(request):
    not_active_filters = get_not_active_filters()
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    fav = get_or_create_favorite(request)
    
    cat_id = request.GET['current_cat']
    filters = request.GET['filters']

    current_cat = Category.objects.get(
        id = cat_id,
    )
    
    products = current_cat.product_set.all()
    # products = Product.objects.filter(
    #     category = current_cat,
    # ) 

    active_filter_items = []

    checked_filters = []

    if len(filters) > 0:
    
        filters = filters.split('_')   
        # attr_list = []
        # attr_items_list = []
        # active_filter_items = []
        for f_item in filters:
            f_item = f_item.split('-')
            attr_id = f_item[0]
            f_item.pop(0)
            products = products.filter(
                attributeitem__id__in = f_item
            )
            for i in f_item:
                checked_filters.append(i)
            
            # attr_list.append(attr_id)
        # print(attr_list)
        # print(attr_items_list)

    print(len(products))
     
    # print(active_filter_items)

    loading_filters = request.GET['loading_filters'] 
    if loading_filters == 'no':
        # products = products[:100]
        return render(request, 'products/blocks/products_list.html', {
            'products': products,
            'fav_main': fav,
            'cart': cart,
            'session_key': session_key,
            'current_cat': current_cat,
        })
    else:
        attr = []
        print('start getting active filters')
        # attribute_items = []
        # attributes = current_cat.attribute_set.all()
        # for a in attributes:
        #     attribute_items.append(a.attributeitem_set.all())
        # print(attribute_items)
        products_ids = list(products.values_list('id', flat = True))
        attr = list(Attributeitem.objects.filter(
            product__id__in = products_ids
        ).values_list('id', flat = True))
        # print('attr is: ', attr)
        # attr = []
        # for product in products: 
        #     attr_items = product.attributeitem_set.all()
        #     for i in attr_items:
        #         if i.id in attr:
        #             pass
        #         else:
        #             attr.append(i.id)
        print('end getting active filters')
        # print(attr)
        return JsonResponse({
            'active_filters': attr,
            'checked_filters': checked_filters,
        }, status = 200)


def load_products_ajax(request):
    print('start category view')
    not_active_filters = get_not_active_filters()
    cart = get_or_create_cart(request)
    session_key = get_session_key(request)
    fav = get_or_create_favorite(request)
    print('cart, session_key, fav got')
    
    # current_cat = Category.objects.get(
    #     id = cat_id,
    # )
    products = Product.objects.all()

    template = 'products/blocks/products_list.html'

    context = {
        'fav_main': fav,
        'cart': cart,
        'session_key': session_key,
        'products': products,
        'not_active_filters': not_active_filters,
    }

    return render(request, template, context)



