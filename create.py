from products.models import * 
import pandas as pd
import unidecode
from django import db

# path = '/Users/noname/jff/santeh/santeh_scrape/test4.csv'
path = '/Users/noname/jff/santeh_main/host/santeh_scrape/new_goods_main.csv'

def createProducts():
    db.connections.close_all()
    deleteall()
    i = 0
    find_dest = 0
    not_find_dest = 0

    data = pd.read_csv(path)
    for index,item in data.iterrows():
        price = item['price']
        # just setting sale price
        if i % 2 == 0:
            sale_price = price / 2
        else:
            sale_price = 0
        # end setting sale price
        name = item['name']
        

        category_name = item['category']
        category_slug = unidecode.unidecode(category_name).lower().strip().replace(' ', '-')

        imgsrc = item['imgsrcnew']
        description = item['description']

        current_category = Category.objects.get_or_create(
            slug = category_slug,
            name = category_name,
        )[0]

        new_product = Product(
            category = current_category,
            name = name,
            price = price,
            sale_price = sale_price,
            description = description,
            imgsrc = imgsrc,
        )
        new_product.save()
        i += 1
        print('created', i, 'products')

        current_attributes = eval(item['attributes'])
        for key in current_attributes:
            current_attr = Attribute.objects.get_or_create(
                category = current_category,
                name = key,
            )[0]
            current_attr.product.add(new_product)

            # new_product.attributes.add(current_attr)
            current_key_value = current_attributes[key]
            if type(current_key_value) == list:
                for attr_name in current_key_value:
                    if len(attr_name) > 0:
                        current_attr_item = Attributeitem.objects.get_or_create(
                            attr = current_attr,
                            name = attr_name,
                        )[0]
                        current_attr_item.product.add(new_product)
                    # new_product.attributes.add(current_attr_item)
            if type(current_key_value) == str:
                if len(current_key_value) > 0:
                    current_attr_item = Attributeitem.objects.get_or_create(
                        attr = current_attr,
                        name = current_key_value,
                    )[0]
                    current_attr_item.product.add(new_product)
                # new_product.attributes.add(current_attr_item)

        

    print('created', i , 'products')


if __name__ == "__main__":
    createProducts()


