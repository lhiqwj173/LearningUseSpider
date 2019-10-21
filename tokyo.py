# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: pycharm
# @Date: 二〇一九年八月六日 星期二 2:20
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08

import asyncio, aiofiles
import os
import sys
import re
from pyquery import PyQuery as pq
from tools import *

# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 本爬虫使用生产者消费者模型，页数获取为递归方式，消费者最大连接数不超过32为宜

imgSearchRe = re.compile("https://my.cdn.tokyo-hot.com/media/.*wlimited\.jpg")

# 主页
hostname = 'https://www.tokyo-hot.com{}'
try:
    url = f'https://www.tokyo-hot.com/product/?page={sys.argv[1]}&vendor=%E6%9D%B1%E7%86%B1'
except:
    url = 'https://www.tokyo-hot.com/product/?page=1&vendor=%E6%9D%B1%E7%86%B1'


async def Producter(url, q2):
    """生产者函数，迭代解析下一页"""
    htmlCode = await get_html_code(url)
    # 解析链接并放入异步队列
    for a in pq(htmlCode)('a.rm'):
        await q2.put(hostname.format(pq(a).attr('href')))

    # 下一页判断
    # nxtpage = 'https://www.tokyo-hot.com/product/'+pq(await w.getHtmlCode())('li.next')('a').attr('href')
    # if nxtpage is not None and nxtpage != url:  # 逻辑不为空且不等于当前请求地址
    #    print(nxtpage)
    #    await Producter(nxtpage, q)


async def Producter2(q2, q):
    while True:
        link = await q2.get()
        print(link)
        htmlCode = await get_html_code(link)
        for _ in imgSearchRe.findall(htmlCode):
            await q.put(_)

        if q2.empty():
            break


async def Consumer(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        link = await q.get()
        dirName = f"tokyo-hot"
        mk_dir(dir=dirName)
        try:
            data = await get_byte(link)
            if not os.path.exists(f'{dirName}/{link.split("media")[-1].replace("/", "")}'):
                async with aiofiles.open(f'{dirName}/{link.split("media")[-1].replace("/", "")}', 'wb') as f:
                    await f.write(data)
            else:
                continue
        except:
            pass
        finally:
            if q.empty():
                break


async def Main():
    q2 = asyncio.Queue(maxsize=2)
    q = asyncio.Queue(maxsize=256)

    task1 = [asyncio.create_task(Producter(url, q2))]
    task2 = [asyncio.create_task(Consumer(q)) for tmp in range(256)]
    task3 = [asyncio.create_task(Producter2(q2, q)) for _ in range(2)]

    await asyncio.wait(task1 + task3 + task2)


asyncio.run(Main())
