# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-09 16:06:15

import asyncio, sys
from pyquery import PyQuery as pq
from tools import *
import re
from functools import partial

# parse = argparse.ArgumentParser(
#     description="xxxxx", prog='xxxxx.py')
# # parse.add_argument('-t', '--tag', type=str, metavar='tagname', help="the tag you wish, example: -t cosplay")
# parse.add_argument('-p', '--page', metavar='n', type=str, help="which page to crawl(clash with -b -a), example: -p 12")
# parse.add_argument('-b', '--between', type=str, nargs=2, metavar='n',
#                    help="page between a and b(include, clash with -p -a), example: -b 2 3")
# parse.add_argument('-a', '--all', action='store_true', help="this flag would download all the page(clash with -p -b)")
# args = parse.parse_args()

# if args.between is not None:
#     a, b = args.between
#     if b < a:
#         print("页数b必须大于a")
#         sys.exit(0)
# else:
#     a, b = None, None
# if args.all is True and args.between is not None:
#     print("a,b标签只能选一个")
#     sys.exit(0)
#     # raise RuntimeError("a,b标签只能选一个")
# if args.between is not None and args.page is not None:
#     print("p,b标签只能选一个")
#     sys.exit(0)

# if args.page is None:
#     args.page = '1'
#     # raise RuntimeError("p,b标签只能选一个")

# 主页
hostname = 'xxxxxxxxxxxxxxxxxxxxxx'
proxy='http://xxx.xxx.xxx.xxx:xxx'

get_html_code_proxy = partial(get_html_code, proxy=proxy)


async def crawler(url, q):
    """生产者函数，迭代解析下一页"""
    try:
        r = await get_html_code_proxy(url)

        # 解析链接并放入异步队列

        for a in pq(r)(".video-list.row.small-up-1.medium-up-2.large-up-4")('.column'):
            if pq(a)('a').attr('href') is not None:
                await q.put(pq(a)('a').attr('href'))

        #下一页判断
        nxtpage = pq(r)('.pagination.text-center.margin-top-4')('li').eq(-2)('a').attr('href')
        if nxtpage not in all_ready_url and nxtpage is not None:  # 逻辑不为空且不等于当前请求地址
           print(nxtpage)
           await crawler(nxtpage, q)
    except:
        pass
    finally:
        pass

async def downloader(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            l = await q.get()
            r = await get_html_code_proxy(l)

            video_url = re.findall("(http://vk.lowbb.xyz/medias/\S+)\"", r)[0]
            with open('file.txt', 'a+') as file:
                file.write(f"{video_url}\n")

        except:
            pass
        finally:
            if q.empty():
                break

async def Main():
    q = asyncio.Queue()

    task1 = asyncio.create_task(crawler(hostname, q))
    #下载协程数量一定要比一次爬取得到的资源数小，否则无法正常结束
    task2 = [asyncio.create_task(downloader(q)) for tmp in range(32)]

    await asyncio.wait([task1] + task2)

if __name__ == '__main__':
    asyncio.run(Main())
