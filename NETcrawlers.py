import requests
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
            pics_url.append(pic_class.find('img')['src'])
        except TypeError:
            pass
    return pics_url

def download_image(url_list, count):
    for index, url in enumerate(url_list):
        filename = str(count) + "_" + str(index) + ".jpg"
        opener = build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
        install_opener(opener)
        urlretrieve(url, filename)

def collect_urls(url_list, filename, PID, IID):
    with open(filename, 'w') as file:
        for url in url_list:
            prefix = 'PID' + str(PID).zfill(6) + '_IID' + str(IID).zfill(6)
            file.write(prefix)
            file.write(' ')
            file.write(url)
            file.write('\n')
            IID += 1

if __name__ == '__main__':    
    pagecount = 60  # Women:60, Men:15
    url_filename = 'NETwomen_urls'
    base_url = 'https://www.net-fashion.net/category/998'
    suffix = [''] + ['/' + str(i) for i in range(2, pagecount+1) ]
    identityCount, productCount = 0, 0
    for i in range(pagecount):
        url = base_url + suffix[i]
        page = get_web_page(url)
        soup = bs(page, 'html.parser')
        products_url = get_product_url(soup)
        
        for product_url in products_url:
            product_page = get_web_page(product_url)
            product_soup = bs(product_page, 'html.parser')
            pics_url = get_pic_url(product_soup)        
            collect_urls(pics_url, url_filename, productCount, identityCount)            
            productCount += 1


        print("page: ", i)

    # url = base_url + suffix[0]
    # page = get_web_page(url)
    # soup = bs(page, 'html.parser')
    # products_url = get_product_url(soup)

    # product_page = get_web_page(products_url[0])
    # product_soup = bs(product_page, 'html.parser')
    # pics_url = get_pic_url(product_soup)


