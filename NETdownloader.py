import requests
import random
import time
import linecache
from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener

epochNum = 10

def read_file(filename, lineNo):
    urls, files = [], []
    EOF = False
    for i in range(epochNum):
        line = linecache.getline(filename, lineNo + i)
        if line == '':
            EOF = True
            break
        
        url, file_out = line.split()
        
    return urls, files, EOF


def download_image(url_list, filename):
    for index, url in enumerate(url_list):
        file_out = filename[index] + '.jpg'
        opener = build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
        install_opener(opener)
        urlretrieve(url, filename)
        time.sleep(0.5) # Maybe wait for a longer time until connecting to the url?


if __name__ == '__main__':
    file_in = ''
    lineNo = 0

    while True:
        url_list, file_list, isEOF = read_file(file_in, lineNo)
        if isEOF:
            print("EOF!!")
            break
        lineNo += epochNum

        var = random.randrange(30, 60)
        time.sleep(var)
        
        for i in range(epochNum):
            download_image(url_list, file_list)










