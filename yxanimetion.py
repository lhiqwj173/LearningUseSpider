#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-10 16:51:03
# @Author  : Anzeme (foxlowm@foxmail.com)
# @Link    : anzeme.com
# @Version : $Id$

import multiprocessing
import os
import re
import sys
from collections import deque
from multiprocessing import Pool

import requests
from pyquery import PyQuery as pq


class Youxia:

    def __init__(self):
        self._word = ['game', 'star', 'meishi',
                      'gaoxiao', 'fengjin', 'news',
                      'dongman', 'qiche', 'other', 'tiyu']
        print("关键字：")  # Print keyword
        print(self._word)
        self._keyword = input("请输入关键字(无须输入''号): ")  # input keyword
        while self._keyword not in self._word:
            print('输入有误，请确认是否正确')
            self._keyword = input('重新输入请继续，退出请键入q：')
            if self._keyword == 'q':
                sys.exit(0)  # What to do next

        self.tuzu = deque()
        self.photo = []
        self.fullweb = []
        self.totle = 0
        self.num = ''
        self.url = 'http://pic.ali213.net'
        self._search_url = 'http://pic.ali213.net/list/%s' % self._keyword

        if os.name == 'nt':
            self._ospath = 'D:\pic'
        else:
            self._ospath = '/Users/Anzeme 1/Pictures'
        self._fpath = os.path.join(self._ospath, self._keyword)  # make dir

        if os.path.exists(self._ospath):
            if os.path.exists(self._fpath):
                pass
            else:
                os.mkdir(self._fpath)
        else:
            os.makedirs(self._fpath)

    def website(self, num=22):
        for n in range(2, num + 1):
            link = 'http://pic.ali213.net/list/%s/index_%s.html' % (self._keyword, n)
            self.fullweb.append(link)

    def html_request(self, url):
        return requests.get(url).text

    def html_data(self, url):
        return requests.get(url, timeout=30).content

    def tuzu_search(self, url, pop=True):
        try:
            q = pq(self.html_request(url))
            for item in q('.box'):
                self.tuzu.append(self.url + pq(item)('a').attr('href'))
                self.num += pq(item)('.fr').text()
            if pop == True:
                self.tuzu.popleft()
        except:
            print("Time out.")

    def jpg_search(self):
        num_count = deque(re.findall(r'\d+', self.num))
        for u in self.tuzu:
            self.photo.append(u)
            for n in range(2, int(num_count[0]) + 1):
                f_l = u[:-5] + '_%s.html' % n
                self.photo.append(f_l)
            self.totle += int(num_count.popleft())

            # if len(num_count) == 0:
            #     break

    def jpg_save(self, url):
        try:
            w = pq(self.html_request(url))
            jpgurl = w('.Ali_Ts1 a').attr('href').split('?')[1]
            jpgname = jpgurl.split('/')[-1]
            jpg_path = os.path.join(self._fpath, jpgname)

            if os.path.isfile(jpg_path):
                print('Photo is exists. Pass')
            else:
                print("Downloading photo: %s" % jpgname)
                with open(jpg_path, 'wb') as f:
                    f.write(self.html_data(jpgurl))
        except AttributeError:
            print('Error Link, Pass.')
        except:
            print("Time out")

    def start(self, full=False, num=None):
        self.tuzu_search(self._search_url)

        if full == True:
            self.website()
            for u in self.fullweb:
                self.tuzu_search(u, pop=False)
        elif isinstance(num, int):
            self.website(num)
            for u in self.fullweb:
                self.tuzu_search(u, pop=False)

        self.jpg_search()

    def download(self):
        print('There are %s jpgs.' % self.totle)
        print('实际下载量可能少于总数(超时链接不计入)')
        choice = input(("按任意键开始下载，输入q退出:"))
        if choice == 'q':
            sys.exit(0)
        p = Pool(multiprocessing.cpu_count())
        try:
            p.map(self.jpg_save, self.photo)
        except:
            print("Time out.")
        finally:
            print("所有下载已完成，图片保存位置'%s'" % self._fpath)


if __name__ == '__main__':
    y = Youxia()
    y.start(full=True)
    y.download()
