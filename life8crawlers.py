import requests
import re
import time
import json
from bs4 import BeautifulSoup as bs
from utils.header import requests_headers

def get_web_page(url):
    header = requests_headers()
    page = requests.get(url, headers=header).content
    soup = bs(page, 'html.parser')
    return soup

def get_product_url(soup):
    prefix_url = 'http://www.life8.com.tw/Shop/'
    products_class = soup.find_all('div', attrs={'class':'itemListDiv'})
    products_url = [prefix_url + product.find('a')['href'] for product in products_class]
    return products_url

def get_pic_url(soup, currentColorCount):

    table_class = soup.find('div', attrs={'id':'itListDetailJson'}).text
    diffColor = json.loads(table_class)['ColorSetupList']
    totalColorCount = len(diffColor)
   
    json_table = diffColor[currentColorCount]['Photos']
    urls = [ resolution['P2'] for resolution in json_table if (resolution['P2'] != '') ]  # 'P1': height 100, 'P2': height 600, 'P3': height 1920

    if (currentColorCount + 1) == totalColorCount:
        return True, urls # Get all different colors

    return False, urls


def collect_urls(url_list, filename, PID, IID):
    with open(filename, 'a') as file:
        for url in url_list:
            prefix = 'PID' + str(PID).zfill(6) + '_IID' + str(IID).zfill(6)
            file.write(prefix)
            file.write(' ')
            file.write(url)
            file.write('\n')
            IID += 1
    return IID


if __name__ == '__main__':
    pageNum = [9, 2]
    url_filename = ['life8_causual_urls', 'life8_formal_urls']
    base_url = ['http://www.life8.com.tw/Shop/itemList.aspx?m=1&p=92&o=0&sa=0&smfp='
                , 'http://www.life8.com.tw/Shop/itemList.aspx?m=1&p=519&o=0&sa=0&smfp=']
    
    for iter in range(2):
        pagecount = pageNum[iter]
        filename = url_filename[iter]
        suffix = [(str(i) + '&') for i in range(1, pagecount+1) ]
        identityCount, productCount, currentColorCount = 0, 0, 0
        getAllColors = True
        for i in range(pagecount):
            print("page: ", i)
            url = base_url[iter] + suffix[i]
            soup = get_web_page(url)
            products_url = get_product_url(soup)
            
            for product_url in products_url:
                product_soup = get_web_page(product_url)
                if getAllColors:
                    currentColorCount = 0                    
                else:
                    currentColorCount += 1
                getAllColors, pics_url = get_pic_url(product_soup, currentColorCount)
                identityCount = collect_urls(pics_url, filename, productCount, identityCount)            
                productCount += 1            
            time.sleep(1)