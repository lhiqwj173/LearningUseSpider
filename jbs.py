# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: PyCharm
# @Date: 2019/8/21 10:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08


import pickle, sys
import argparse
from pyquery import PyQuery as pq
from tools import *
from functools import partial

#获取tag名称
with open("javbusAllTags", 'rb') as file:
    dictTag = pickle.load(file)
#print(dictTag)

PARSE = argparse.ArgumentParser(
    description="downloader for hentaiAinime, default runtime crawl the index page", prog='jbs.py')
PARSE.add_argument('-t', '--tag', type=str, metavar='tagname', help="crawler the tag of movie")
PARSE.add_argument('-s', '--show', action="store_true", help="show all the tag")
PARSE.add_argument('-p', '--page', metavar='n', type=str, help="which page to crawl(clash with -b -a), example: -p 12")
PARSE.add_argument('-e', '--end', metavar='n', type=str, help="end num")
#PARSE.add_argument('-b', '--between', type=str, nargs=2, metavar='n',
#                   help="page between a and b(include, clash with -p -a), example: -b 2 3")
PARSE.add_argument('-a', '--all', action='store_true', help="this flag would download all the page(clash with -p -b)")
PARSE.add_argument('-u', '--url', type=str, metavar='url', help="address to crawler")
args = PARSE.parse_args()
	
if args.show == True:
    print(dictTag)
    sys.exit(0)
# if args.between is not None:
#     BANANA, CAR = args.between
#     if CAR < BANANA:
#         print("页数b必须大于a")
#         sys.exit(0)
# else:
#     BANANA, CAR = None, None
# if args.all is True and args.between is not None:
#     print("a,b标签只能选一个")
#     sys.exit(0)

# if args.between is not None and args.page is not None:
#     print("p,b标签只能选一个")
#     sys.exit(0)

#获取下载链接，默认为首页

#请求用cookie和header
cookies = {
           #"__cfduid": "dd29e013b776090606255d0e835bf844a1570958478",
           #"PHPSESSID": "1hv1et9jo5ts9jhc6el6vu9b93",
           "existmag": "mag",
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}

proxy = 'http://127.0.0.1:1080'

get_html_code_proxy = partial(get_html_code, proxy=proxy)
get_byte_proxy = partial(get_byte, proxy=proxy)

async def crawler(duilie, url):
    """生产者，迭代解析下一页"""
    try:
        print("当前抓取\t"+url)
        r = await get_html_code_proxy(url, cookies=cookies, headers=headers)
        #放入队列
        for _ in pq(r)('a.movie-box'):
            await duilie.put(pq(_).attr('href'))

        #下一页判断
        if args.all == True:
            nxtpage = f"https://www.dmmsee.bid{pq(r)('a#next').attr('href')}"
            if nxtpage != url and pq(r)('a#next').attr('href') is not None:  # 逻辑不为空且不等于当前请求地址
                print(nxtpage)
                await crawler(duilie, nxtpage)

        if args.end is not None:
            nxtpage = f"https://www.dmmsee.bid{pq(r)('a#next').attr('href')}"
            if nxtpage != url and pq(r)('a#next').attr('href') is not None and url.split("/")[-1] != args.end:
                print(nxtpage)
                await crawler(duilie, nxtpage)

    except TypeError:
        print(f"lastpage\t{nxtpage}")
    except:
        print("Crawler Unknow Error")

async def downloader(duilie, url):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            #获取链接
            boxLink = await duilie.get()
            #图片存放目录
            tag = url.split('/')[-1]
            youMa_wuMa = url.split('/')[3]
            dirName = f"javbus/{youMa_wuMa}/{dictTag[youMa_wuMa][tag]}"
            mk_dir(dirName)
            jpgName = f"{dirName}/{boxLink.split('/')[-1]}.jpg"

            #下载块
            if not os.path.exists(jpgName):
                for _ in pq(await get_html_code_proxy(boxLink))('a.bigImage'):
                    #图片名称
                    jpgUrl = pq(_).attr('href')
                    #写入数据
                    with open(jpgName, 'wb') as fileWrite:
                        fileWrite.write(await get_byte_proxy(jpgUrl))
                    print(f"{jpgName}\tLeft{duilie.qsize()}")
            else:
                raise RuntimeError("Exists")
        except RuntimeError as e:
            print(e)
        except:
            print("Unknow Error")
        finally:
            #队列为空则停止循环
            if duilie.empty():
                break

async def downloader_index(duilie, i):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            # 获取链接
            boxLink = await duilie.get()
            # 图片存放目录
            dirName = f"javbus/test_all"
            mk_dir(dirName)
            jpgName = f"{dirName}/{boxLink.split('/')[-1]}.jpg"

            # 下载块
            for _ in pq(await get_html_code_proxy(boxLink))('a.bigImage'):
                # 图片名称
                jpgUrl = pq(_).attr('href')
                # 写入数据
                with open(jpgName, 'wb') as fileWrite:
                    fileWrite.write(await get_byte_proxy(jpgUrl))
                print(f"{jpgName}")

        except:
            print("Unknow Error")
        finally:
            if duilie.empty():
                break

async def main():
    """封装主函数，方便多进程调用"""
    #队列深度
    duilie = asyncio.Queue()

    if args.url is not None:
        if args.page is not None:
            url = args.url+f"/{args.page}"
        else:
            url = args.url
        c = [asyncio.create_task(downloader(duilie, url)) for _ in range(8)]

    else:
        if args.page is not None:
            #url = f"https://www.dmmsee.bid/uncensored/studio/3j/{args.page}"
            url = f"https://www.dmmsee.bid/page/{args.page}"
        else:
            #url = "https://www.dmmsee.bid/uncensored/studio/3j"
            url = "https://www.dmmsee.bid"
        c = [asyncio.create_task(downloader_index(duilie, _)) for _ in range(30)]

    #url = "https://www.dmmsee.bid"
    #c = [asyncio.create_task(downloader_index(duilie, _)) for _ in range(30)]
    #封装协程p
    p = asyncio.create_task(crawler(duilie, url))


    await asyncio.wait([p]+c)

if __name__ == "__main__":
	asyncio.run(main())
