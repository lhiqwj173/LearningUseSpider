# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: pycharm
# @Date: 二〇一九年八月六日 星期二 2:20
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08

import asyncio, aiofiles
import sys
import re
from tools import Web
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# 本爬虫使用生产者消费者模型，页数获取为递归方式，消费者最大连接数不超过32为宜

imgSearchRe = re.compile("https://my.cdn.tokyo-hot.com/media/.*wlimited\.jpg")

# 主页
hostname = 'https://www.tokyo-hot.com{}'
url = f'https://www.tokyo-hot.com/product/{sys.argv[1]}/'

async def Producter(q):
    """生产者函数，迭代解析下一页"""
    w = Web(url)
    
    picUrl = imgSearchRe.findall(await w.getHtmlCode())
    for a in picUrl:
        await q.put(a)


async def Consumer(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        w = Web(await q.get())

        async with aiofiles.open(f'tokyo-hot/{w.url.split("media")[-1].replace("/","")}', 'wb') as f:
            await f.write(await w.getByte())
            
        if q.empty():
            break
            
async def Main():
    q = asyncio.Queue()

    task1 = [asyncio.create_task(Producter(q))]
    task2 = [asyncio.create_task(Consumer(q)) for tmp in range(256)]

    await asyncio.wait(task1 + task2)


asyncio.run(Main())
