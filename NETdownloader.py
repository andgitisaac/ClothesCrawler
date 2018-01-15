import os
import requests
import urllib.request
import random
import time

# headers = [('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]

def requests_headers():
    head_connection = ['Keep-Alive','close']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = {
        'Connection':head_connection[random.randrange(0,len(head_connection))],
        'Accept':head_accept[0],
        'Accept-Language':head_accept_language[random.randrange(0,len(head_accept_language))],
        'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))],
    }
    return header 

def download_image(url, filename, file_in, lineNo):
    file_out = filename + '.jpg'
    log_out = file_in + '.log'
    cwd = os.getcwd()
    hdr = requests_headers()

    try:
        raw = requests.get(url, headers=hdr)
        with open(os.path.join(os.getcwd(), 'PHOTO', file_out), 'wb') as image:
            image.write(raw.content)
        time.sleep(0.5) # Maybe wait for a longer time until connecting to the url?
        return False

    except requests.exceptions.RequestException as err:
        print(err)
        with open(log_out, 'a') as log:
            log.write(filename)
            log.write(' ')
            log.write(url)
            log.write(' ')
            log.write(str(lineNo))
            log.write(' ')
            log.write(str(err))
        return True

if __name__ == '__main__':
    file_in = 'NETwomen_urls'
    lineNo = 0

    f = open(file_in, 'r')
    for line in f:
        file_out, url = line.strip('\n').split()
            
        exceptionRaise = download_image(url, file_out, file_in, lineNo)
            
        if exceptionRaise:
            print("Exception Raise at line {}. Halt for 1800 secs".format(lineNo))
            time.sleep(1800)
        elif (lineNo % 100) == 0 and lineNo != 0: # Sleep for an hour for every 100 photos
            print("At line {}. Halt for 3600 secs".format(lineNo))
            time.sleep(3600)
        elif (lineNo % 10) == 0 and lineNo != 0: # Sleep for a while for every 10 photos
            var = random.randrange(60, 120)
            print("At line {}. Halt for {} secs".format(lineNo, var))
            time.sleep(var)
        lineNo += 1        
    f.close()
            
        