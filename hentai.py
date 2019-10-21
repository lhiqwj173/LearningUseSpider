# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08

import sys
from pyquery import PyQuery as pq
from tools import *
import re
import argparse

VIDEOSEARCH = re.compile('http[s]?:\/\/.*\.mp4')

PARSE = argparse.ArgumentParser(
    description="downloader for hentaiAinime, default runtime crawl the index page", prog='hentai.py')
PARSE.add_argument('-t', '--tag', type=str, metavar='tagname', help="the tag you wish, example: -t cosplay")
PARSE.add_argument('-p', '--page', metavar='n', type=str, help="which page to crawl(clash with -b -a), example: -p 12")
PARSE.add_argument('-b', '--between', type=str, nargs=2, metavar='n',
                   help="page between a and b(include, clash with -p -a), example: -b 2 3")
PARSE.add_argument('-a', '--all', action='store_true', help="this flag would download all the page(clash with -p -b)")
args = PARSE.parse_args()

if args.between is not None:
    BANANA, CAR = args.between
    if CAR < BANANA:
        print("页数b必须大于a")
        sys.exit(0)
else:
    BANANA, CAR = None, None
if args.all is True and args.between is not None:
    print("a,b标签只能选一个")
    sys.exit(0)
    # raise RuntimeError("a,b标签只能选一个")
# if args.all is True and args.page is not None:
#    print("a,p标签只能选一个")
#    sys.exit(0)
# raise RuntimeError("a,p标签只能选一个")
if args.between is not None and args.page is not None:
    print("p,b标签只能选一个")
    sys.exit(0)


async def crawler(url, q):
    """解析协程，用于解析首层链接"""
    try:
        print(f"当前抓取: {url}")
        r = await get_html_code(url)
        # print(r)
        # 解析链接并放入异步队列
        for _ in pq(r)('.item.tvshows.infinite-item.pop_info'):
            await q.put(pq(_)('a').attr('href'))

        # 分支：所有
        if args.all:
            if pq(r)('.infinite-more-link').attr('href') is not None and pq(r)('h2').text() != 'Nothing Found':
                nxtpage = pq(r)('.infinite-more-link').attr('href')
                await crawler(nxtpage, q)
        # 分支： 部分
        else:
            if CAR:
                if pq(r)('.infinite-more-link').attr('href') is not None and pq(r)('h2').text() != 'Nothing Found':
                    nxtpage = pq(r)('.infinite-more-link').attr('href')
                    if CAR != re.findall("\/page\/(\d*)", nxtpage)[0]:
                        await crawler(nxtpage, q)
    except:
        print("Error CrwalerOne")


async def crawler_two(q, q2):
    """解析协程2，用以解析二层链接，可多开"""
    while True:
        try:
            # 解析二层视频地址
            for _ in pq(await get_html_code(await q.get()))('div .season_m.animation-4'):
                await q2.put(pq(_)('a').attr('href'))
        except:
            print("Error CrawlerTwo")
        finally:
            # 队列为空，结束循环
            if q.empty():
                break


async def writer(q2, tag):
    """处理协程，可多开"""
    while True:
        try:
            VideoLink = pq(await get_html_code(await q2.get()))('#option-1')('iframe').attr("src")
            TargetHtmlSource = await get_html_code(VideoLink)

            TargetLink = VIDEOSEARCH.search(TargetHtmlSource).group(0)
            with open(f'{tag}.txt', 'a+', encoding='utf-8') as file:
                file.write(f"{TargetLink}\n")
                print(f"{TargetLink}\t Done, Left {q2.qsize()}")
        except:
            print("Error Writer")
        finally:
            if q2.empty():
                break


async def main():
    q = asyncio.Queue()
    q2 = asyncio.Queue()

    if args.tag:
        tag = args.tag
        if args.page:
            apple = f'https://hentaimama.com/advance-search/page/{args.page}/?genres_filter%5B%5D={tag}&submit=Submit'
        elif BANANA:
            apple = f'https://hentaimama.com/advance-search/page/{BANANA}/?genres_filter%5B%5D={tag}&submit=Submit'
        else:
            apple = f'https://hentaimama.com/advance-search/?genres_filter%5B%5D={tag}&submit=Submit'

    else:
        tag = "top"
        if args.page:
            apple = f'https://hentaimama.com/trending/page/{args.page}'
        elif BANANA:
            apple = f'https://hentaimama.com/trending/page/{BANANA}'
        else:
            apple = 'https://hentaimama.com/trending'

    crawler1 = asyncio.create_task(crawler(apple, q))
    crawler2 = [asyncio.create_task(crawler_two(q, q2)) for _ in range(2)]
    writer1 = [asyncio.create_task(writer(q2, tag)) for _ in range(4)]

    await asyncio.wait([crawler1] + crawler2 + writer1)


asyncio.run(main())
