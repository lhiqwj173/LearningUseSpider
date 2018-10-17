#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: VsCode
# @Date: 2018-09-10 15:51:03
# @Last Modified by:   anzeme
# @Last Modified time: 2018-09-10 15:51:03

import aiohttp
import sys
import uvloop
"""windows不可用"""

import asyncio
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

import time
from html_parse import *
"""导入自写模块"""

t0 = time.time()
"""开始计时"""
url = sys.argv[1]
path_name = sys.argv[2]
"""取得终端命令参数/URL/dirPath"""

#mode = input('Img_mode(True/False): ')
"""是否使用图片模式"""

dirCheck(path_name)
"""检测目录"""


async def product(q):
    """生产函数，解析链接放入队列"""
    async with aiohttp.ClientSession() as session:
        html = await fetch(url, session)
        img_link = parse_link(html, img=True)
        for _ in img_link:
            await q.put(_)
            print('生产者 ==> 已放入 {}'.format(_))

        """队列完成，添加中止信号"""
        for i in range(4):
            await q.put(None)

        print("已全部生产完毕，开始阻塞队列")
        await q.join()
        print("生产结束，等待程序中止")


async def consume(q, i):
    """消费函数，队列取值进行下载"""
    async with aiohttp.ClientSession() as session:
        """开始提取链接"""
        while True:
            """每次提取结束发送完成信号"""
            link = await q.get()
            print("协程 {} 开始提取链接 {}".format(i, link))
            if link is None:
                q.task_done()
                break
            else:
                await downloader(link, session, path_name)
                q.task_done()

        print("协程 {} 号已完成任务".format(i))


async def main(loop):
    """创建4个生产者协程"""

    q = asyncio.Queue(maxsize=8)
    consumer = [
        loop.create_task(consume(q, i)) for i in range(4)
    ]

    """创建生产者协程"""
    prod = loop.create_task(product(q))

    """等待全部协程完成"""
    """因为wait只能接受一个参数，所以把prod转换成列表再和生产者进行切片合并"""
    await asyncio.wait([prod] + consumer)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

print(time.time() - t0)

"""结束计时"""
