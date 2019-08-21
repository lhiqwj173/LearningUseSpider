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
            dirName = f"javbus/无码/玩法/{tag}"
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
        "https://www.busjav.net/uncensored/genre/6",
        "https://www.busjav.net/uncensored/genre/1o",
        "https://www.busjav.net/uncensored/genre/w",
        "https://www.busjav.net/uncensored/genre/28",
        "https://www.busjav.net/uncensored/genre/10u",
        "https://www.busjav.net/uncensored/genre/1c2",
        "https://www.busjav.net/uncensored/genre/6w",
        "https://www.busjav.net/uncensored/genre/iz",
        "https://www.busjav.net/uncensored/genre/117",
        "https://www.busjav.net/uncensored/genre/zk",
        "https://www.busjav.net/uncensored/genre/22",
        "https://www.busjav.net/uncensored/genre/6t",
        "https://www.busjav.net/uncensored/genre/62",
        "https://www.busjav.net/uncensored/genre/wo",
        "https://www.busjav.net/uncensored/genre/8e",
        "https://www.busjav.net/uncensored/genre/161",
        "https://www.busjav.net/uncensored/genre/12u",
        "https://www.busjav.net/uncensored/genre/kr",
        "https://www.busjav.net/uncensored/genre/b6",
        "https://www.busjav.net/uncensored/genre/yk",
        "https://www.busjav.net/uncensored/genre/sl",
        "https://www.busjav.net/uncensored/genre/10w",
        "https://www.busjav.net/uncensored/genre/162",
        "https://www.busjav.net/uncensored/genre/2g",
        "https://www.busjav.net/uncensored/genre/15z",
        "https://www.busjav.net/uncensored/genre/11i",
        "https://www.busjav.net/uncensored/genre/1cv",
        "https://www.busjav.net/uncensored/genre/11s",
        "https://www.busjav.net/uncensored/genre/12a",
        "https://www.busjav.net/uncensored/genre/14l",
        "https://www.busjav.net/uncensored/genre/rk",
        "https://www.busjav.net/uncensored/genre/11l",
        "https://www.busjav.net/uncensored/genre/125",
        "https://www.busjav.net/uncensored/genre/we",
        "https://www.busjav.net/uncensored/genre/122",
        "https://www.busjav.net/uncensored/genre/10q",
        "https://www.busjav.net/uncensored/genre/1b8",
        "https://www.busjav.net/uncensored/genre/m3",
        "https://www.busjav.net/uncensored/genre/gre120",
        "https://www.busjav.net/uncensored/genre/gre121",
        "https://www.busjav.net/uncensored/genre/gre122",
        "https://www.busjav.net/uncensored/genre/gre123",
        "https://www.busjav.net/uncensored/genre/gre124",
        "https://www.busjav.net/uncensored/genre/gre125",
        "https://www.busjav.net/uncensored/genre/gre126",
        "https://www.busjav.net/uncensored/genre/gre127",
        "https://www.busjav.net/uncensored/genre/gre128",
        "https://www.busjav.net/uncensored/genre/gre129",
        "https://www.busjav.net/uncensored/genre/gre130",
        "https://www.busjav.net/uncensored/genre/gre131",
        "https://www.busjav.net/uncensored/genre/gre132",
        "https://www.busjav.net/uncensored/genre/gre133",
        "https://www.busjav.net/uncensored/genre/gre134",
        "https://www.busjav.net/uncensored/genre/gre135",
        "https://www.busjav.net/uncensored/genre/gre136",
        "https://www.busjav.net/uncensored/genre/gre137",
        "https://www.busjav.net/uncensored/genre/gre138",
        "https://www.busjav.net/uncensored/genre/gre139",
        "https://www.busjav.net/uncensored/genre/gre140",
        "https://www.busjav.net/uncensored/genre/gre141",
    ]

    p = [Process(target=MultiprocessStart, args=(url, url.split('/')[-1])) for url in urlList]
    for _ in p:
        _.start()
    for _ in p:
        _.join()

