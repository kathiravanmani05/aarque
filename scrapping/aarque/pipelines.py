import logging
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aarque.models import Product

class AarquePipeline:
    def __init__(self):
        self.engine = create_engine('mariadb+mariadbconnector://sdk:TKnApQsKErGlXv6H@localhost/sdk_aarque')
        #self.engine = create_engine('mysql://root:root@localhost/aarque')
        self.Session = sessionmaker(bind=self.engine)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        with self.Session() as session:
            try:
                # Process images
                if 'images' in item and item['images']:
                    images = [img.replace('odoo-1fbbc.kxcdn.com/web/image/product.product/', '').split('/')[0] for img in item['images']]
                else:
                    images = []

                # Find existing record by SKU
                record = session.query(Product).filter_by(sku=item['sku']).first()

                if record:
                    self.logger.info(f"Updating existing product with SKU: {item['sku']}")
                    record.url_scraped = item.get('url_scraped', None)
                    record.name = item.get('name', None)
                    record.price = item.get('price', 0)
                    record.percent_discount = item.get('percent_discount', 0.0)
                    record.price_discount = item.get('price_discount', 0.0)
                    record.tax = item.get('tax', 0.0)
                    record.price_included_taxes = item.get('price_included_taxes', 0.0)
                    record.price_mt2 = item.get('price_mt2', 0.0)
                    record.price_mtl = item.get('price_mtl', 0.0)
                    record.stock_1 = item.get('stock_1', 0)
                    record.stock_2 = item.get('stock_2', 0)
                    record.stock_3 = item.get('stock_3', 0)
                    record.stock_comentarie_1 = item.get('stock_comentarie_1', None)
                    record.stock_comentarie_2 = item.get('stock_comentarie_2', None)
                    record.stock_comentarie_3 = item.get('stock_comentarie_3', None)
                    record.images = json.dumps(images)
                    record.category = item.get('category', None)
                    record.route_product = item.get('route_product', None)
                    record.short_description = item.get('short_description', None)
                    record.long_description = item.get('long_description', None)
                    record.pdf = json.dumps(item.get('pdf', []))
                    record.length = item.get('length', None)
                    record.width = item.get('width', None)
                    record.height = item.get('height', None)
                    record.weight = item.get('weight', None)
                    record.main_color = item.get('main_color', None)
                    record.glossy_or_matte = item.get('glossy_or_matte', None)
                    record.main_material = item.get('main_material', None)
                    record.origen = item.get('origen', None)
                    spider.logger.info("Record updated successfully.")
                else:
                    self.logger.info(f"Creating new product with SKU: {item['sku']}")
                    new_record = Product(
                        sku=item.get('sku'),
                        name=item.get('name'),
                        url_scraped=item.get('url_scraped', None),
                        price=item.get('price', 0),
                        percent_discount=item.get('percent_discount', 0.0),
                        price_discount=item.get('price_discount', 0.0),
                        tax=item.get('tax', 0.0),
                        price_included_taxes=item.get('price_included_taxes', 0.0),
                        price_mt2=item.get('price_mt2', 0.0),
                        price_mtl=item.get('price_mtl', 0.0),
                        stock_1=item.get('stock_1', 0),
                        stock_2=item.get('stock_2', 0),
                        stock_3=item.get('stock_3', 0),
                        stock_comentarie_1=item.get('stock_comentarie_1', None),
                        stock_comentarie_2=item.get('stock_comentarie_2', None),
                        stock_comentarie_3=item.get('stock_comentarie_3', None),
                        images=json.dumps(images),
                        category=item.get('category', None),
                        route_product=item.get('route_product', None),
                        short_description=item.get('short_description', None),
                        long_description=item.get('long_description', None),
                        pdf=json.dumps(item.get('pdf', [])),
                        length=item.get('length', None),
                        width=item.get('width', None),
                        height=item.get('height', None),
                        weight=item.get('weight', None),
                        main_color=item.get('main_color', None),
                        glossy_or_matte=item.get('glossy_or_matte', None),
                        main_material=item.get('main_material', None),
                        origen=item.get('origen', None),
                    )
                    session.add(new_record)
                    spider.logger.info("New record created successfully.")

                session.commit()
            except Exception as e:
                session.rollback()
                self.logger.error(f"Failed to process item: {e}", exc_info=True)

        return item
