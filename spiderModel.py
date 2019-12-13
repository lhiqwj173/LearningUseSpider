# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-13 12:07:56
from tools import *
if os.name == "posix":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parse = argparse.ArgumentParser(
    description="downloader for fc2ppvfanclub picture, default runtime crawl the first page", prog='xxxxxxxx.py')
parse.add_argument('-p', '--page',default='1', metavar='指定页数', type=str, help="指定页数进行下载")
parse.add_argument('-e', '--end', type=str, metavar='结束页数', help="指定结束页数")
parse.add_argument('-a', '--all', action='store_true', help="下载全站")
parse.add_argument('--proxy', type=str, metavar='"地址:端口"', help="启用代理，暂不支持socks,example: --proxy=\"http://127.0.0.1:1080\"")
args = parse.parse_args()

    # raise RuntimeError("p,b标签只能选一个")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


hostname = "xxxxxxxxxxxxxx" # 自行修改

if args.proxy != None:
    get_html_code_proxy = partial(get_html_code, proxy=args.proxy, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, proxy=args.proxy, headers=headers)
else:
    get_html_code_proxy = partial(get_html_code, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, headers=headers)

async def crawler(url, q):
    """生产者函数，迭代解析下一页"""
    try:
        r = await get_html_code_proxy(url)

        # 解析链接并放入异步队列，自行修改解析目标
        for a in pq(r)(".video-list.row.small-up-1.medium-up-2.large-up-4")('.column'):
            if pq(a)('a').attr('href') is not None:
                await q.put(pq(a)('a').attr('href'))

        if args.all is True:
            #下一页判断，自行修改
            nxtpage = pq(r)('.pagination.text-center.margin-top-4')('li').eq(-2)('a').attr('href')
            if nxtpage is not None and nxtpage != url:  # 逻辑不为空且不等于当前请求地址
               print(nxtpage)
               await crawler(nxtpage, q)

    except BaseException as e:
        print(e)

async def downloader(q):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            # 如果不需要二次解析的话
            filesavepath="xxxxxxxxxxxxx" # 自行修改
            await get_byte_named_proxy(session, await q.get(), filesavepath)

            #r = await get_html_code_proxy(await q.get())
            #url = xxxxxxxxxxxxxxxxxxxxx
            #filesavepath="xxxxxxxxxxxxx"
            #await get_byte_named_proxy(session, url, filesavepath)

        except BaseException as e:
            print(e)
        finally:
            if q.empty():
                break

async def Main():
    q = asyncio.Queue()

    task1 = asyncio.create_task(crawler(hostname, q))
    #下载协程数量一定要比一次爬取得到的资源数小，否则无法正常结束
    async with aiohttp.ClientSession(trust_env=True) as session:
        task2 = [asyncio.create_task(downloader(q, session)) for tmp in range(8)]
        await asyncio.wait([task1] + task2)

if __name__ == '__main__':
    asyncio.run(Main())
