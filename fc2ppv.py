# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08

import asyncio
import sys
from pyquery import PyQuery as pq
from tools import Web

# 本爬虫使用生产者消费者模型，页数获取为递归方式，消费者最大连接数不超过32为宜

# 主页
hostname = 'http://fc2fans.club{}'
try:
    url = f'http://fc2fans.club/index.php?m=content&c=index&a=lists&catid=12&page={sys.argv[1]}'
except:
    url = f'http://fc2fans.club/index.php?m=content&c=index&a=lists&catid=12&page=1'


async def Producter(url, q):
    """生产者函数，迭代解析下一页"""
    w = Web(url)

    # 解析链接并放入异步队列
    for a in pq(await w.getHtmlCode())('.title.title-info')('a'):
        await q.put(hostname.format(pq(a).attr('href')))

    # 下一页判断
    #nxtpage = pq(await w.getHtmlCode())('#pages')('.a1').eq(-1).attr('href')
    #if nxtpage is not None and nxtpage != url:  # 逻辑不为空且不等于当前请求地址
    #    print(nxtpage)
    #    await Producter(nxtpage, q)


async def Consumer(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        w = Web(await q.get())
        picUrl = hostname.format(pq(await w.getHtmlCode())(
            'div.col-sm-8')('#thumbpic').parent().attr('href'))

        w2 = Web(picUrl)
        await w2.saveFile()

        if q.empty():
            break

async def Main():
    q = asyncio.Queue(maxsize=16)

    task1 = [asyncio.create_task(Producter(url, q))]
    task2 = [asyncio.create_task(Consumer(q)) for tmp in range(4)]

    await asyncio.wait(task1 + task2)


asyncio.run(Main())
