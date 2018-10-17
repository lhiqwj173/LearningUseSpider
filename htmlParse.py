#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: VsCode
# @Date: 2018-09-10 09:39:58
# @Last Modified by:   anzeme
# @Last Modified time: 2018-09-10 09:39:58

import re
import aiofiles
from pyquery import PyQuery as pq
import os

img_search = re.compile(r'[a-zA-z]+://[^\s]*big.jpg')
a_search = re.compile(r'[a-zA-z]+://[^\s]*')


def dirCheck(path):
    """目录检测"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(path+' NOT EXISTS >> CREATED')
    else:
        print(path+" EXISTS >> CONTINUTE")


async def fetch(url, session, data=False):
    """解析网页"""
    async with session.get(url, proxy='http://127.0.0.1:1081') as s:
        """选择返回Content还是Html"""
        if data:
            return await s.read()
        else:
            return await s.text()


def parse_link(html_data, img=False):
    """提取网页链接/图片链接"""
    # with open('leak_html.txt', 'w') as f:
    #    f.write(html_data)
    if img:
        return img_search.findall(html_data)
    return a_search.findall(html_data)


async def downloader(url, session, path):
    """下载器"""
    name = url.split('/')[-1]
    fullpath = os.path.join(path, name)
    data = await fetch(url, session, data=True)
    """返回Content数据并写入"""
    async with aiofiles.open(fullpath, 'wb') as aiof:
        await aiof.write(data)
    print(name + " => ok\n")
