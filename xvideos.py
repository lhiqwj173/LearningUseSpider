#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: notepad++
# @Date: 2019-07-04 星期四 12:23
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期四 11:52

"""UseManage
Usage:
  xvideos.py <tag>

Options:
<tag>   关键字，不加为insemination，中文英文亦可
"""

import re, asyncio, sys
from pyquery import PyQuery as pq
from tools import Web

linkSearch = re.compile('html5player.setVideoUrlHigh\(.+\)')  #xvideo视频地址
try:
    keyword = str(sys.argv[1])
except:
    keyword = 'insemination'

indexUrl = f'https://www.xvideos.com/?k={keyword}&p=0'
hostUrl = 'https://www.xvideos.com{}'


async def Producter(q, url, c):
    w = Web(url)
    r = await w.getHtmlCode()
    for _ in pq(r)('.thumb'):
        linkName = hostUrl.format(pq(_)('a').attr('href'))
        await q.put(linkName)

    while True:
        w = Web(f'https://www.xvideos.com/?k={keyword}&p={str(c)}')
        print(w.url)
        r = await w.getHtmlCode()

        if c > int(re.findall("\d+", pq(r)('title').text())[0]):
            break

        for _ in pq(r)('.thumb'):
            linkName = hostUrl.format(pq(_)('a').attr('href'))
            await q.put(linkName)
        c += 1


async def Consumer(q):
    while True:
        url = await q.get()

        w = Web(url)
        r = await w.getHtmlCode()

        downloadLink = linkSearch.findall(r)[0].split("'")[1]
        with open(f'{keyword}.txt', 'a+') as file:
            file.write(f'{downloadLink}\n')

        if q.empty():
            break


async def Main():
    q = asyncio.Queue(maxsize=16)
    c = 1  # 页数记数器

    task1 = [asyncio.create_task(Producter(q, indexUrl, c))]
    task2 = [asyncio.create_task(Consumer(q)) for _ in range(8)]

    await asyncio.wait(task1 + task2)


if __name__ == '__main__':
    asyncio.run(Main())
