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
            dirName = f"javbus/有码/行为/{tag}"
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
                

async def Main(url):
    q = asyncio.Queue(maxsize=30)
    q2 = asyncio.Queue(maxsize=30)

    tag = url.split('/')[-1]
    task1 = [asyncio.create_task(Producter(url, q))]
    task2 = [asyncio.create_task(Producter2(q, q2)) for _ in range(30)]
    task3 = [asyncio.create_task(Consumer(q2, tag)) for tmp in range(30)]

    await asyncio.wait(task1 + task3 + task2)

def MultiprocessStart(url):
    asyncio.run(Main(url))

if __name__ == "__main__":
    #有码行为
    urlList = [
        "https://www.busjav.net/genre/4w",
        "https://www.busjav.net/genre/4t",
        "https://www.busjav.net/genre/4j",
        "https://www.busjav.net/genre/47",
        "https://www.busjav.net/genre/46",
        "https://www.busjav.net/genre/45",
        "https://www.busjav.net/genre/42",
        "https://www.busjav.net/genre/3q",
        "https://www.busjav.net/genre/3l",
        "https://www.busjav.net/genre/3f",
        "https://www.busjav.net/genre/2h",
        "https://www.busjav.net/genre/24",
        "https://www.busjav.net/genre/1z",
        "https://www.busjav.net/genre/1s",
        "https://www.busjav.net/genre/1r",
        "https://www.busjav.net/genre/1p",
        "https://www.busjav.net/genre/1o",
        "https://www.busjav.net/genre/1j",
        "https://www.busjav.net/genre/19",
        "https://www.busjav.net/genre/x",
        "https://www.busjav.net/genre/u",
        "https://www.busjav.net/genre/r",
        "https://www.busjav.net/genre/n",
        "https://www.busjav.net/genre/h",
        "https://www.busjav.net/genre/5",
        "https://www.busjav.net/genre/4",
        "https://www.busjav.net/genre/6m",
    ]

    p = Pool(8)
    p.map(MultiprocessStart, urlList)

