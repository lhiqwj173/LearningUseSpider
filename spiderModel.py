# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08

import asyncio, sys
from pyquery import PyQuery as pq
from tools import *


parse = argparse.ArgumentParser(
    description="xxxxx", prog='xxxxx.py')
# parse.add_argument('-t', '--tag', type=str, metavar='tagname', help="the tag you wish, example: -t cosplay")
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
if args.between is not None and args.page is not None:
    print("p,b标签只能选一个")
    sys.exit(0)

if args.page is None:
    args.page = '1'
    # raise RuntimeError("p,b标签只能选一个")

# 主页
hostname = 'xxxxx'
proxy='xxxxx'


async def crawler(url, q):
    """生产者函数，迭代解析下一页"""
    try:
        r = await getHtmlCode(url)
        # 解析链接并放入异步队列

        #for a in pq(r)('.title.title-info')('a'):
        #    await q.put(hostname.format(pq(a).attr('href')))

        #下一页判断
        # nxtpage = pq(html)('#pages')('.a1').eq(-1).attr('href')
        # if nxtpage is not None and nxtpage != url:  # 逻辑不为空且不等于当前请求地址
        #    print(nxtpage)
        #    await crawler(nxtpage, q)pip
    except:
        pass
    finally:
        print("crawler Done")

async def downloader(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            r = await getHtmlCode(await q.get())
            #picUrl = hostname.format(pq(r)(
            #    'div.col-sm-8')('#thumbpic').parent().attr('href'))

            #imgSave = f"download/{picUrl.split('/')[-1]}"
            
            #with open(imgSave, 'wb') as file:
            #    file.write(await getByte(picUrl))
        except:
            pass
        finally:
            if q.empty():
                break

async def Main():
    q = asyncio.Queue()

    task1 = asyncio.create_task(crawler(url, q))
    #下载协程数量一定要比一次爬取得到的资源数小，否则无法正常结束
    task2 = [asyncio.create_task(downloader(q)) for tmp in range(8)]

    await asyncio.wait([task1] + task2)

if __name__ == '__main__':
    asyncio.run(Main())