# -*- coding: utf-8 -*-
import os
import re
import logging
import requests
from urllib import error
from bs4 import BeautifulSoup

def find_img(url):
    ReList = []
    try:
        html = requests.get(url, allow_redirects=False)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    ReList.append(i.get_text())
        return ReList

def dowmload(html, name, numimg):
    num = 0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    for img in pic_url:
        try:
            if img is not None:
                pic = requests.get(img, timeout=7)
            else:
                continue
        except BaseException:
            logging.error('Download image unsucessefully')
            continue
        else:
            string = name + r'\\' + name + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            logging.info('Sucesseful download No. %s %s image... '%(str(num+1), name))
            num += 1
        if num >= numimg:
            return

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s: %(message)s')
    header = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'Upgrade-Insecure-Requests': '1'
    }
    rqs = requests.Session()
    rqs.headers = header
    img_name = ['cat', 'dog', 'rabbit', 'panda']
    num = 1 # default download number of images are 1 (each class), if need more images, please change num
    url_name = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='
    pn = '&pn='
    for name in list(img_name):
        url = url_name + str(name) + pn
        imgList = find_img(url)
        folder = os.path.exists(str(name))
        if folder != 1:
            os.mkdir(str(name))
        count = 0
        url_b = url
        while count < num:
            try:
                url = url_b + str(count)
                result = rqs.get(url, timeout=10, allow_redirects=False)
            except error.HTTPError as e:
                logging.error('Connect error')
                count = count + 60
            else:
                dowmload(result.text, str(name), num)
                count = count + 60

    print('All images download sucessefully!')
    print()
