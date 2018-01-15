import requests
import re
import time
from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
from bs4 import BeautifulSoup as bs

def get_web_page(url):
    header = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=header)
    page = urlopen(req)

    return page

def get_product_url(soup):    
    products_class = soup.find_all('div', attrs={'class':'main_name'})
    products_url = [product.a['href'] for product in products_class]
    return products_url

def get_pic_url(soup):
    pics_class = soup.find_all('p', attrs={'align':'center'})

    pics_url = []
    for pic_class in pics_class:
        try:
            urlStr = pic_class.find('img')['src'].split('?')[0]
            if bool(re.search(r'(?:hair|warmheat|warmtech|/001.jpg|LONEY|WOOL|sp|BonhuiUy|NT|．)', urlStr)):
                # These keywords in the url means this photo is useless
                continue
            pics_url.append(urlStr)
        except TypeError:
            pass
    return pics_url

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

# def download_image(url_list, count):
#     for index, url in enumerate(url_list):
#         filename = str(count) + "_" + str(index) + ".jpg"
#         opener = build_opener()
#         opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
#         install_opener(opener)
#         urlretrieve(url, filename)

if __name__ == '__main__':    
    pageNum = [60, 15]  # Women:60, Men:15
    url_filename = ['NETwomen_urls', 'NETmen_urls']
    base_url = ['https://www.net-fashion.net/category/998', 'https://www.net-fashion.net/category/999']
    
    for iter in range(1, 2):
        pagecount = pageNum[iter]
        filename = url_filename[iter]
        suffix = [''] + ['/' + str(i) for i in range(2, pagecount+1) ]
        identityCount, productCount = 0, 0
        for i in range(pagecount):
            url = base_url[iter] + suffix[i]
            page = get_web_page(url)
            soup = bs(page, 'html.parser')
            products_url = get_product_url(soup)
            
            for product_url in products_url:
                product_page = get_web_page(product_url)
                product_soup = bs(product_page, 'html.parser')
                pics_url = get_pic_url(product_soup)        
                identityCount = collect_urls(pics_url, filename, productCount, identityCount)            
                productCount += 1
            print("page: ", i)
            time.sleep(1)

