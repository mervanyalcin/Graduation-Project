from email import charset
import mysql.connector
import requests
from lxml import html
import datetime
import json

# cnx = mysql.connector.connect(user='u0528528_userABM', password='TNdp86X7KLut93B',host='94.73.147.224',database='u0528528_ABMGP')
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='mervanyalcin', charset='utf8')
cursor = cnx.cursor()
query = (
    "INSERT INTO products (product_title, product_url, crawling_date, product_brand, product_img, retailer_name, product_id, product_availability,"
    " product_price, product_price_2, product_position, product_category, product_subcategory) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    
url = 'https://www.trendyol.com/erkek-sneaker-x-g2-c1172'
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'sec-ch-ua-platform': 'macOS',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
res = requests.get(url, headers=header)
dom = html.fromstring(res.content.decode(encoding='utf-8'))
product_urls = dom.xpath('//div[@class="p-card-wrppr"]/div/a/@href')
data_id = dom.xpath('//div[@class="prdct-cntnr-wrppr"]/div/@data-id')

for no, url in enumerate(product_urls, 1):
    product_url = ("https://www.trendyol.com" + url)
    product_page_res = requests.get(product_url, headers=header)
    product_dom = html.fromstring(product_page_res.content.decode(encoding='utf-8'))
    crawling_date = datetime.date.today()

    product_brand = str(product_dom.xpath('//h1[@class="pr-new-br"]//text()')[0].strip())

    try:
        product_price = float(product_dom.xpath('//span[@class="prc-dsc"]/text()')[0].split(' TL')[0].replace(',', '.'))
    except Exception as e:
        try:
            product_price = float(
                product_dom.xpath('//span[@class="prc-slg"]/text()')[0].split(' TL')[0].replace(',', '.'))
        except:
            product_price = float(
                product_dom.xpath('//span[@class="prc-org"]/text()')[0].split(' TL')[0].replace(',', '.'))

    try:
        product_price_2 = float(
            product_dom.xpath('//span[@class="prc-org"]/text()')[0].split(' TL')[0].replace(',', '.'))
    except Exception:
        try:
            product_price_2 = float(
                product_dom.xpath('//span[@class="prc-slg prc-slg-w-dsc"]/text()')[0].split(' TL')[0].replace(',', '.'))
        except Exception:
            product_price_2 = float(
                product_dom.xpath('//span[@class="prc-slg"]/text()')[0].split(' TL')[0].replace(',', '.'))
            if product_price_2 == product_price:
                product_price_2 = None

    product_availability_xpath = '//div[@class="add-to-basket-button-text"]/text()'
    product_json_xpath = '//script[@type="application/javascript"]/text()'

    for script in product_dom.xpath(product_json_xpath):
        if '__PRODUCT_DETAIL_APP_INITIAL_STATE__' in str(script):
            product_json = json.loads(script.split('STATE__=')[1].split(';window.TY')[0])
            product_img = str('https://cdn.dsmcdn.com' + product_json['product']['images'][0])
            product_id = str(product_json['product']['id'])

    product_title = str(
        product_brand + ' ' + product_dom.xpath('//h1[@class="pr-new-br"]/span/text()')[0].strip()).encode().decode(
        encoding='utf-8')
    merchant = str(product_dom.xpath('//a[@class="merchant-text"]/text()')[0].strip())
    if product_dom.xpath(product_availability_xpath):
        product_availability = True
    position = no
    retailer_name = "Trendyol"

    # print('RETAILER::', retailer_name, '  PRODUCT_ID::', product_id, '  PRODUCT_BRAND::', product_brand,
    #     '  PRODUCT_PRICE::', product_price, '  PRODUCT_PRICE_2::', product_price_2,
    #     '  PRODUCT_TITLE::', product_title, '  PRODUCT_POSITION::', no, '  PRODUCT_CRAWLING_DATE::', crawling_date,
    #     '  PRODUCT_URL::',  product_url, '  PRODUCT_MERCHANT::', merchant,
    #     '  PRODUCT_AVAILABILITY::', product_availability,
    #     '  PRODUCT_IMAGE_URL::', product_img)

    print(product_title)

    product_position = "1"
    product_category = "Empty"
    product_subcategory = "Empty"

    cursor.execute(query, (
    product_title, product_url, crawling_date, product_brand, product_img, retailer_name, product_id,
    product_availability, product_price, product_price_2, product_position, product_category, product_subcategory))

cnx.commit()
cursor.close()
cnx.close()
