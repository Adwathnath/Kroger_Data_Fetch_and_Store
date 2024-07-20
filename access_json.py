from datetime import datetime
from DBworks import *

#transform data.json
def access(data, event_type):
    try:
        products = data['data']
        for product in products:
            product_id = product['productId']
            upc = product['upc']
            product_page_uri = product['productPageURI']
            brand = product['brand']
            categories = ', '.join(product['categories'])
            country_origin = product['countryOrigin']
            description = product['description']
            times = datetime.now()
            time_str = event_type+" "+times.strftime('%Y-%m-%d %I:%M %p')

            #insert product
            insert_product_query = "insert into products values (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (product_id, upc, product_page_uri, brand, categories, country_origin, description, time_str)
            iud(insert_product_query,val)

            #insert images
            for image in product['images']:
                perspective = image['perspective']
                for size in image['sizes']:
                    image_size = size['size']
                    url = size['url']

                    insert_image_query = "insert into images values( %s, %s, %s, %s, %s)"
                    valm = (product_id, perspective, image_size, url, time_str)
                    iud(insert_image_query,valm)

            #insert items data
            for item  in product['items']:
                item_id = item['itemId']
                size = item['size']
                fulfillment = item['fulfillment']
                curbside = fulfillment['curbside']
                delivery = fulfillment['delivery']
                in_store = fulfillment['inStore']
                ship_to_home = fulfillment['shipToHome']

                insert_item_query = "insert into items values(%s, %s, %s, %s, %s, %s, %s, %s)"
                val_items = (product_id, item_id, size, curbside, delivery, in_store, ship_to_home, time_str)
                iud(insert_item_query, val_items)  



    except Exception as e:
        print("Exception occured :",e)        