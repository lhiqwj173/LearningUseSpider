# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: PyCharm
# @Date: 2019/8/21 10:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08


import asyncio, aiofiles
import os
import sys
import re
from pyquery import PyQuery as pq
from tools import Web
from multiprocessing import Pool,Process

async def Producter(url, q):
    """生产者函数，迭代解析下一页"""
    w = Web(url)

    htmlCode = await w.getHtmlCode()
    # 解析链接并放入异步队列
    for a in pq(htmlCode)('a.movie-box'):
        await q.put(pq(a).attr('href'))

    # 下一页判断
    try:
        nxtpage = "https://www.busjav.net"+pq(htmlCode)('a#next').attr('href')
        if nxtpage is not None and nxtpage != url:  # 逻辑不为空且不等于当前请求地址
            print(nxtpage)
            await Producter(nxtpage, q)
    except TypeError:
        print("Last Page")

async def Producter2(q, q2):
    while True:
        try:
            boxItem = await q.get()
            print(boxItem)
            w2 = Web(boxItem)

            htmlCode = await w2.getHtmlCode()
            for _ in pq(htmlCode)('a.bigImage'):
                await q2.put([boxItem,pq(_).attr('href')])
        except:
            pass
        finally:
            if q.empty():
                break


async def Consumer(q2, tag):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            imgUrl = await q2.get()
            w3 = Web(imgUrl[1])
            dirName = f"javbus/无码/行为/{tag}"
            Web.mkDir(dirName)

            data = await w3.getByte()
            imgName = f"{dirName}/{imgUrl[0].split('/')[-1]}.jpg"
            if not os.path.exists(imgName):
                async with aiofiles.open(imgName, 'wb') as f:
                    await f.write(data)
            else:
                continue
        except:
            pass
        finally:
            if q2.empty():
                break
                

async def Main(url, tag):
    q = asyncio.Queue(maxsize=30)
    q2 = asyncio.Queue(maxsize=30)

    task1 = [asyncio.create_task(Producter(url, q))]
    task2 = [asyncio.create_task(Producter2(q, q2)) for _ in range(30)]
    task3 = [asyncio.create_task(Consumer(q2, tag)) for tmp in range(30)]

    await asyncio.wait(task1 + task3 + task2)

def MultiprocessStart(url, tag):
    asyncio.run(Main(url, tag))

if __name__ == "__main__":
    urlList = [
        "https://www.busjav.net/uncensored/genre/i",
        "https://www.busjav.net/uncensored/genre/34",
        "https://www.busjav.net/uncensored/genre/3x",
        "https://www.busjav.net/uncensored/genre/11a",
        "https://www.busjav.net/uncensored/genre/c2",
        "https://www.busjav.net/uncensored/genre/v4",
        "https://www.busjav.net/uncensored/genre/5u",
        "https://www.busjav.net/uncensored/genre/11e",
        "https://www.busjav.net/uncensored/genre/uc",
        "https://www.busjav.net/uncensored/genre/14w",
        "https://www.busjav.net/uncensored/genre/141",
        "https://www.busjav.net/uncensored/genre/110",
        "https://www.busjav.net/uncensored/genre/kp",
        "https://www.busjav.net/uncensored/genre/tc",
        "https://www.busjav.net/uncensored/genre/kv",
        "https://www.busjav.net/uncensored/genre/10p",
        "https://www.busjav.net/uncensored/genre/12p",
        "https://www.busjav.net/uncensored/genre/124",
        "https://www.busjav.net/uncensored/genre/11p",
        "https://www.busjav.net/uncensored/genre/13a",
        "https://www.busjav.net/uncensored/genre/134",
        "https://www.busjav.net/uncensored/genre/12x",
        "https://www.busjav.net/uncensored/genre/128",
        "https://www.busjav.net/uncensored/genre/14d",
        "https://www.busjav.net/uncensored/genre/2c",
        "https://www.busjav.net/uncensored/genre/12l",
        "https://www.busjav.net/uncensored/genre/13r",
        "https://www.busjav.net/uncensored/genre/14v",
        "https://www.busjav.net/uncensored/genre/gre083",
        "https://www.busjav.net/uncensored/genre/gre084",
        "https://www.busjav.net/uncensored/genre/gre085",
        "https://www.busjav.net/uncensored/genre/gre086",
        "https://www.busjav.net/uncensored/genre/gre087",
        "https://www.busjav.net/uncensored/genre/gre088",
        "https://www.busjav.net/uncensored/genre/gre089",
        "https://www.busjav.net/uncensored/genre/gre090",
        "https://www.busjav.net/uncensored/genre/gre091",
        "https://www.busjav.net/uncensored/genre/gre092",
        "https://www.busjav.net/uncensored/genre/gre093",
        "https://www.busjav.net/uncensored/genre/gre094",
        "https://www.busjav.net/uncensored/genre/gre095",
        "https://www.busjav.net/uncensored/genre/gre096",
        "https://www.busjav.net/uncensored/genre/gre097",
        "https://www.busjav.net/uncensored/genre/gre098",
        "https://www.busjav.net/uncensored/genre/gre099",
        "https://www.busjav.net/uncensored/genre/gre100",
        "https://www.busjav.net/uncensored/genre/gre101",
        "https://www.busjav.net/uncensored/genre/gre102",
        "https://www.busjav.net/uncensored/genre/gre103",
        "https://www.busjav.net/uncensored/genre/gre104",
        "https://www.busjav.net/uncensored/genre/gre105",
        "https://www.busjav.net/uncensored/genre/gre106",
        "https://www.busjav.net/uncensored/genre/gre107",
        "https://www.busjav.net/uncensored/genre/gre108",
        "https://www.busjav.net/uncensored/genre/gre109",
        "https://www.busjav.net/uncensored/genre/gre110",
        "https://www.busjav.net/uncensored/genre/gre111",
        "https://www.busjav.net/uncensored/genre/gre112",
        "https://www.busjav.net/uncensored/genre/gre113",
        "https://www.busjav.net/uncensored/genre/gre114",
        "https://www.busjav.net/uncensored/genre/gre115",
        "https://www.busjav.net/uncensored/genre/gre116",
        "https://www.busjav.net/uncensored/genre/gre117",
        "https://www.busjav.net/uncensored/genre/gre118",
        "https://www.busjav.net/uncensored/genre/gre119",
        "https://www.busjav.net/uncensored/genre/gre154",
    ]

    p = [Process(target=MultiprocessStart, args=(url, url.split('/')[-1])) for url in urlList]
    for _ in p:
        _.start()
    for _ in p:
        _.join()


