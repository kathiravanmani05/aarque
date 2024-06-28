from shop.models import Product
import json

def fetch_categories():
    unique_categories = Product.objects.values_list('category', flat=True).distinct()
    return unique_categories

def fetch_products(category):
    products = Product.objects.filter(category=category).values('name', 'sku','images','price')
    for product in products:
        # Assuming 'images' field is a JSON string of image IDs
        images = product['images']
       
        if images:
            image_ids = json.loads(images)
            print(image_ids)
            # Generate URLs based on your URL pattern for images
            product['images'] =image_ids[0]
            print(product)
        else:
            product['images'] = []
    return products

def fetch_product_detail(sku):
    product = Product.objects.filter(sku=sku).first()
    if product:
        # Assuming images are stored as a JSON string in the database
        images = product.images  # This should be a JSON string like '["51774"]'
        images_list = json.loads(images) if images else []  # Convert JSON string to Python list
        product.images = images_list  # Replace JSON string with Python list of image IDs or URLs
    return product

def search_product(search_variable):
    if not search_variable:
        return None
    product = Product.objects.filter(sku=search_variable).values().first()
    return product