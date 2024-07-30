import scrapy,re,os,requests
from scrapy import Request


class AarqueScrapingSpider(scrapy.Spider):
    name = "aarque_scraping"
    allowed_domains = ["aarque.co.nz"]
    start_urls = ["https://www.aarque.co.nz/shop"]

    def parse(self, response):
        links = response.xpath('//*[@itemprop="name"]/@href').extract()
        for link in links:
            url = 'https://www.aarque.co.nz' + link
            
            yield Request(url, callback=self.data_link)
        next_page = response.xpath('//*[contains(text(),"Next")]/@href').extract_first()
        if next_page:
            next_page_url = 'https://www.aarque.co.nz' + next_page
            yield Request(next_page_url, callback=self.parse)
    def check_file_in_folder(self, folder, file):
        return os.path.exists(os.path.join(folder, file))
    
    def save_image(self, temp_images, folder="images"):
       
        for url in temp_images:
            abs_url = 'https://'+url
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_name = abs_url.replace('https://odoo-1fbbc.kxcdn.com/web/image/product.product/','').split('/')[0]
            if self.check_file_in_folder(folder, file_name):
                continue
            filepath = os.path.join(folder, file_name)

            response = requests.get(abs_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                    print(f"Image saved as {filepath}")
            else:
                print(f"Failed to download image from {abs_url}")


    def data_link(self, response):
        def clean_text(text):
            if text:
                return re.sub(r'\s+', ' ', text).strip()
            return text

        name = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        sku = response.xpath('//*[@itemprop="sku"]/text()').extract_first()
        category = response.xpath('//*[@class="cat_name"]/li/a/span/text()').extract_first()
        price = response.xpath('//*[@class="oe_currency_value"]/text()').extract_first()

        items = response.xpath('//*[@class="product_attachments"]//table//tbody/tr')
        data_dict = {}  # Initialize an empty dictionary

        for item in items:
            key = item.xpath('.//th//text()').extract_first()
            value = item.xpath('.//td//text()').extract_first()
            
            if key and value:  # Ensure both key and value are not None
                clean_key = clean_text(key)
                clean_value = clean_text(value)
                data_dict[clean_key] = clean_value
        details = data_dict
        images =[]
        image = response.xpath('//*[@itemprop="image"]/@src').extract_first().replace('//','')
        short = response.xpath('//*[@class="product_attachments"]//text()').extract()
        short_descriptions = [item.strip() for item in short if item.strip()]
        short_description = '\n'.join(short_descriptions)
        images.append(image)
        self.save_image(images)
        
       
        yield {
            'sku': sku,
            'name': name,
            'url_scraped': response.url,
            'price': price,
            'category': category,
            'percent_discount': 0.00,
            'price_discount': 0.00,
            'tax': 0.00,
            'price_included_taxes': 0.00,
            'price_mt2': 0.00,
            'price_mtl': 0.00,
            'stock_1': 1,
            'stock_2': None,
            'stock_3': None,
            'stock_comentarie_1': None,
            'stock_comentarie_2': None,
            'stock_comentarie_3': None,
            'images': images,
            'route_product': None,
            'short_description': short_description,
            'long_description': details,
            'pdf': None,
            'length': None,
            'width': None,
            'height': None,
            'weight': None,
            'main_color': None,
            'glossy_or_matte': None,
            'main_material': None,
            'origen': None
            }