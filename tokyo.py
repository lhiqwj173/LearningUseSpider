# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: pycharm
# @Date: 二〇一九年八月六日 星期二 2:20
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08

import asyncio, aiofiles
import sys
import re
from pyquery import PyQuery as pq
from tools import Web

# 本爬虫使用生产者消费者模型，页数获取为递归方式，消费者最大连接数不超过32为宜

imgSearchRe = re.compile("https://my.cdn.tokyo-hot.com/media/.*wlimited\.jpg")

# 主页
hostname = 'https://www.tokyo-hot.com{}'
try:
    url = f'https://www.tokyo-hot.com/product/?page={sys.argv[1]}&vendor=%E6%9D%B1%E7%86%B1'
except:
    url = 'https://www.tokyo-hot.com/product/?page=1&vendor=%E6%9D%B1%E7%86%B1'

async def Producter(url, q):
    """生产者函数，迭代解析下一页"""
    w = Web(url)

    # 解析链接并放入异步队列
    for a in pq(await w.getHtmlCode())('a.rm'):
        await q.put([hostname.format(pq(a).attr('href')), pq(a)('img').attr('alt')])

    # 下一页判断
    nxtpage = hostname.format(pq(await w.getHtmlCode())('li.next')('a').attr('href'))
    if nxtpage is not None and nxtpage != url:  # 逻辑不为空且不等于当前请求地址
        print(nxtpage)
        await Producter(nxtpage, q)


async def Consumer(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        link = await q.get()
        w = Web(link[0])
        picUrl = imgSearchRe.findall(await w.getHtmlCode())
        print(w.url)

        dirName = f"tokyo-hot"
        Web.mkDir(dir=dirName)
        for a in picUrl:
            w2 = Web(a)
            data = await w2.getByte()
            #print(w2.url)

            async with aiofiles.open(f'{dirName}/{a.split("/")[-2]}.jpg', 'wb') as f:
                await f.write(data)

        if q.empty():
            break

async def Main():
    q = asyncio.Queue(maxsize=32)

    task1 = [asyncio.create_task(Producter(url, q))]
    task2 = [asyncio.create_task(Consumer(q)) for tmp in range(4)]

    await asyncio.wait(task1 + task2)


asyncio.run(Main())
