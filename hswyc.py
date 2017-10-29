#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/4 16:23
# @Author  : Aries
# @Site    : anzeme.com
# @File    : hswyc.py
# @Software: PyCharm Community Edition

import os, multiprocessing,requests

from multiprocessing import Pool
from pyquery import PyQuery as pq
from datetime import datetime

class Hswyc:

    def __init__(self):
        self._domain = 'http://www.verydm.com'
        self._starturl = 'http://www.verydm.com/manhua/heisewuyecao'
        self._eachpart = []
        self._eachpage = []
        self._time = datetime.now()
        self._total = 0
        self._path = '/Users/Anzeme 1/Pictures/heisewuyecao/'

    def html_text(self, url):
        return requests.get(url).text

    def html_data(self, url):
        return requests.get(url).content

    def index_parse(self):
        self._eachpart = [self._domain+pq(a).attr('href') for a in \
                          pq(self.html_text(self._starturl))('.chapters')('.clearfix')('a')]

    def part_parse(self, url):
        pagec = pq(self.html_text(url))('.pagination')('a').eq(-2).html().split('.')[-1]
        for c in range(1,int(pagec)+1):
            full_url = '%s&p=%s' %(url, c)
            self.img_save(full_url)

    def img_save(self, url):
        jpgurl = pq(self.html_text(url))('#mainImage2').attr('src')
        jpgname = jpgurl.split('/')[-1]

        jpgpath = self._path+jpgurl.split('/')[-2]
        savepath = os.path.join(jpgpath,jpgname)

        if not os.path.exists(jpgpath):
            os.makedirs(jpgpath)
        if os.path.isfile(savepath):
           print('Exist,Pass')
        else:
            print('Download %s %s' %(jpgurl.split('/')[-2],jpgname))
            with open(savepath, 'wb') as f:
                f.write(self.html_data(jpgurl))

    def start(self):
        self.index_parse()
        print("Starting downloading")
        p = Pool(multiprocessing.cpu_count())
        p.map(self.part_parse, self._eachpart)
        end = datetime.now()
        use_time = self._time - end
        print("Spend %s seconds" %use_time)
        print("All downloading is done. Have Fun")

if __name__ == '__main__':
    h = Hswyc()
    h.start()
    
