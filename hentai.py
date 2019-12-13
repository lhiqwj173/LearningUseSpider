# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-13 12:39:25

from tools import *
if os.name == "posix":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

VIDEOSEARCH = re.compile('http[s]?:\/\/.*\.mp4')

PARSE = argparse.ArgumentParser(
    description="downloader for hentaiAinime, default runtime crawl the index page", prog='hentai.py')
PARSE.add_argument('-t', '--tag', type=str, metavar='tagname', help="the tag you wish, example: -t cosplay")
PARSE.add_argument('-p', '--page', metavar='n', type=str, help="which page to crawl(clash with -b -a), example: -p 12")
PARSE.add_argument('-a', '--all', action='store_true', help="下载全站，配合-e使用")
parse.add_argument('--proxy', type=str, metavar='"地址:端口"', help="启用代理，暂不支持socks,example: --proxy=\"http://127.0.0.1:1080\"")
parse.add_argument('-e', '--end', type=str, metavar='结束页数', help="指定结束页数")
args = PARSE.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


if args.proxy != None:
    get_html_code_proxy = partial(get_html_code, proxy=args.proxy, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, proxy=args.proxy, headers=headers)
else:
    get_html_code_proxy = partial(get_html_code, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, headers=headers)

async def crawler(url, q):
    """解析协程，用于解析首层链接"""
    try:
        print(f"当前抓取: {url}")
        r = await get_html_code_proxy(url)
        # print(r)
        # 解析链接并放入异步队列
        for _ in pq(r)('.item.tvshows.infinite-item.pop_info'):
            await q.put(pq(_)('a').attr('href'))

        # 分支：所有
        if args.all:
            if pq(r)('.infinite-more-link').attr('href') is not None and pq(r)('h2').text() != 'Nothing Found' and str(re.findall("\/page\/(\d*)", nxtpage)[0]) != str(args.end):
                nxtpage = pq(r)('.infinite-more-link').attr('href')
                await crawler(nxtpage, q)

    except BaseException as e:
        print(e)


async def crawler_two(q, q2):
    """解析协程2，用以解析二层链接，可多开"""
    while True:
        try:
            # 解析二层视频地址
            for _ in pq(await get_html_code_proxy(await q.get()))('div .season_m.animation-4'):
                await q2.put(pq(_)('a').attr('href'))
        except BaseException as e:
            print(e)
        finally:
            # 队列为空，结束循环
            if q.empty():
                break


async def writer(q2, tag):
    """处理协程，可多开"""
    while True:
        try:
            VideoLink = pq(await get_html_code_proxy(await q2.get()))('#option-1')('iframe').attr("src")
            TargetHtmlSource = await get_html_code_proxy(VideoLink)

            TargetLink = VIDEOSEARCH.search(TargetHtmlSource).group(0)
            with open(f'{tag}.txt', 'a+', encoding='utf-8') as file:
                file.write(f"{TargetLink}\n")
                print(f"{TargetLink}\t Done")
        except BaseException as e:
            print(e)
        finally:
            if q2.empty():
                break


async def main():
    q = asyncio.Queue()
    q2 = asyncio.Queue()

    if args.tag:
        if args.page:
            url = f'https://hentaimama.com/advance-search/page/{args.page}/?genres_filter%5B%5D={args.tag}&submit=Submit'
        else:
            url = f'https://hentaimama.com/advance-search/?genres_filter%5B%5D={args.tag}&submit=Submit'

    else:
        tag = "top"
        if args.page:
            url = f'https://hentaimama.com/trending/page/{args.page}'
        else:
            url = 'https://hentaimama.com/trending'

    crawler1 = asyncio.create_task(crawler(url, q))
    crawler2 = [asyncio.create_task(crawler_two(q, q2)) for _ in range(2)]
    writer1 = [asyncio.create_task(writer(q2, tag)) for _ in range(4)]

    await asyncio.wait([crawler1] + crawler2 + writer1)


asyncio.run(main())
