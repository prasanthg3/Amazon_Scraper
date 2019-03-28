import csv
import json
import os
import random
import sys
from time import sleep
from lxml import html
import requests
import pandas as pd

user_agent_list = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) \
                        Gecko/20100101 Firefox/61.0',
                       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
                       'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) \
                        Gecko/20100101 Firefox/61.0',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/60.0.3112.113 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/63.0.3239.132 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/66.0.3359.117 Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) \
                        AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 \
                        Safari/603.3.8',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 \
                        Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 \
                        Safari/537.36']
def parse_product(url):
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    page = requests.get(url, headers=headers)

    for i in range(1):
        sleep(random.randint(1, 3))
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            #XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P")\
                    #or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_RATING = '//i[contains(@data-hook,"average-star-rating")]/span[contains(@class, "a-icon-alt")]/text()'
            XPATH_NO_OF_RVWS= '//h2[@data-hook="total-review-count"]//text()'
            XPATH_ASIN = '//li/@data-asin//text()'
            XPATH_SELLER = '//div[@id="merchant-info"]/a[1]//text()'
            
            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            #RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_RATING = doc.xpath(XPATH_RATING)
            RAW_NO_OF_RVWS = doc.xpath(XPATH_NO_OF_RVWS)
            RAW_SELLER = doc.xpath(XPATH_SELLER)[0]

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            #ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
            RATING = ''.join(RAW_RATING).strip() if RAW_RATING else None
            REVIEWS =  ''.join(RAW_NO_OF_RVWS).strip() if RAW_NO_OF_RVWS else None
            #ASIN = ''.join(RAW_ASIN).strip() if RAW_ASIN else None
            REVIEWS = REVIEWS.split(" ")[0]
            RATING = RATING.split(" ")[0]

            if not NAME:
                raise ValueError('Captcha?')

            data = {'ASIN':url.split("/dp/")[1].split('/')[0],
                    'NAME':NAME,
                    'SELLER':RAW_SELLER,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'AVG_RATING':RATING,
                    'NO_OF_REVIEWS':REVIEWS,
                   }

            return data

        except Exception as e:
            print(e)
def parse_p_url_list(url):
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    page = requests.get(url, headers=headers)
    
    data=[]
    for i in range(1):
        sleep(random.randint(1, 3))
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href'
            RAW_NAME = doc.xpath(XPATH_NAME)
            NAME = [x for x in RAW_NAME if RAW_NAME]
           
            return NAME


        except Exception as e:
            print(e)
def parse_nxt_page (url):
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    page = requests.get(url, headers=headers)
    sleep(random.randint(1, 3))
    doc = html.fromstring(page.content)
    XPATH_NEXT = '//li[@class="a-last"]/a/@href'
    RAW_NEXT = doc.xpath(XPATH_NEXT)
    if len(RAW_NEXT)!=0:
        RAW_NEXT=RAW_NEXT[0]
    return 'https://www.amazon.in'+str(RAW_NEXT)
page_urls=['https://www.amazon.in/s?i=amazonbasics&srs=6637738031&lo=list&page=2&qid=1552930120&ref=sr_pg_1']
i=0
product_lst=[]
while page_urls[i]!='https://www.amazon.in[]':
    product_url_list=[]
    page_urls+=[parse_nxt_page(page_urls[i])]
    product_url_list+=parse_p_url_list(page_urls[i])
    i+=1
    for product in product_url_list:
        product_lst.append(parse_product(product))
    print("  total products scrapped:  {0}      page No:  {1}".format(len(product_lst),i))
print("done")
df=pd.DataFrame(product_lst)
df.to_csv('Amazon_basics_products.csv', index=False)