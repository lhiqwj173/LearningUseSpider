#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: notepad++
# @Date: 2019-07-04 星期四 12:23
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期四 11:52


import re, sys
from pyquery import PyQuery as pq
from tools import *
import argparse

# 终端参数解析
parse = argparse.ArgumentParser(
    description="downloader for xvideos , default runtime crawl the index page", prog='xvideos.py')
parse.add_argument('-t', '--tag', default='cosplay', type=str, metavar='tagname',
                   help="the tag you wish, example: -t cosplay")
parse.add_argument('-p', '--page', metavar='n', type=str, help="which page to crawl(clash with -b -a), example: -p 12")
parse.add_argument('-b', '--between', type=str, nargs=2, metavar='n',
                   help="page between a and b(include, clash with -p -a), example: -b 2 3")
parse.add_argument('-a', '--all', action='store_true', help="this flag would download all the page(clash with -p -b)")
args = parse.parse_args()

if args.between is not None:
    a, b = args.between
    if b < a:
        print("页数b必须大于a")
        sys.exit(0)
else:
    a, b = None, None
if args.all is True and args.between is not None:
    print("a,b标签只能选一个")
    sys.exit(0)
    # raise RuntimeError("a,b标签只能选一个")
if args.all is True and args.page is not None:
    print("a,p标签只能选一个")
    sys.exit(0)
    # raise RuntimeError("a,p标签只能选一个")
if args.between is not None and args.page is not None:
    print("p,b标签只能选一个")
    sys.exit(0)

# xvideo视频地址
linkSearch = re.compile('html5player.setVideoUrlHigh\(.+\)')

# 主机名
hostname = 'https://www.xvideos.com{}'


async def crawler(duilie, url, count):
    """页面解析函数"""
    print(f"当前抓取: {url}")
    # 当前页解析
    for _ in pq(await get_html_code(url))('.thumb'):
        await duilie.put(hostname.format(pq(_)('a').attr('href')))

    # 下一页循环
    if args.all is True:
        while True:
            newUrl = f'https://www.xvideos.com/?k={args.tag}&p={str(count)}'
            print(f"下一页: {newUrl}")
            r = await get_html_code(newUrl)
            # 寻找当前页数，判断计数器是否大于
            if count > int(re.findall("\d+", pq(r)('title').text())[0]):
                break
            for _ in pq(r)('.thumb'):
                await duilie.put(hostname.format(pq(_)('a').attr('href')))
            count += 1


async def downloader(duilie):
    while True:
        url = await duilie.get()

        downloadLink = linkSearch.findall(await get_html_code(url))[0].split("'")[1]
        with open(f'{args.tag}.txt', 'a+') as file:
            file.write(f'{downloadLink}\n')

        if duilie.empty():
            break


async def Main():
    q = asyncio.Queue(maxsize=16)

    if a:
        indexUrl = f'https://www.xvideos.com/?k={args.tag}&p={a}'
        c = a
    elif args.page:
        indexUrl = f'https://www.xvideos.com/?k={args.tag}&p={args.page}'
        c = args.page
    else:
        indexUrl = f'https://www.xvideos.com/?k={args.tag}&p=0'
        c = 1

    task1 = asyncio.create_task(crawler(q, indexUrl, c))
    task2 = [asyncio.create_task(downloader(q)) for _ in range(8)]

    await asyncio.wait([task1] + task2)


if __name__ == '__main__':
    asyncio.run(Main())
