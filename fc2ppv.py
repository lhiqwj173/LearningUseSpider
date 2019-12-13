# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-13 12:05:10

from tools import *
if os.name == "posix":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parse = argparse.ArgumentParser(
    description="downloader for fc2ppvfanclub picture, default runtime crawl the first page", prog='fc2ppv.py')
parse.add_argument('-p', '--page',default='1', metavar='指定页数', type=str, help="指定页数进行下载")
parse.add_argument('-e', '--end', type=str, metavar='结束页数', help="指定结束页数")
parse.add_argument('-a', '--all', action='store_true', help="下载全站")
parse.add_argument('--proxy', type=str, metavar='"地址:端口"', help="启用代理，暂不支持socks,example: --proxy=\"http://127.0.0.1:1080\"")
args = parse.parse_args()

    # raise RuntimeError("p,b标签只能选一个")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}

# 主页
hostname = 'http://fc2fans.club{}'

if args.proxy != None:
    get_html_code_proxy = partial(get_html_code, proxy=args.proxy, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, proxy=args.proxy, headers=headers)
else:
    get_html_code_proxy = partial(get_html_code, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, headers=headers)

async def parseLink(url, duilie):
    """生产者函数，迭代解析下一页"""
    print(f"当前抓取: {url}")
    r = await get_html_code_proxy(url)
    # 解析链接并放入异步队列

    for a in pq(r)('.title.title-info')('a'):
        await duilie.put(hostname.format(pq(a).attr('href')))

    # 下一页判断
    if args.all is True:
        nxtpage = pq(r)('#pages')('.a1').eq(-1).attr('href')
        if nxtpage is not None and nxtpage != url and str(nxtpage[-1]) != str(args.end):  # 逻辑不为空且不等于当前请求地址
            await parseLink(nxtpage, duilie)


async def downloader(duilie, n, session):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            r = await get_html_code_proxy(await duilie.get())
            picUrl = hostname.format(pq(r)(
                'div.col-sm-8')('#thumbpic').parent().attr('href'))

            imgSave = f"download/{picUrl.split('/')[-1]}"
            await get_byte_named(session, picUrl, imgSave, proxy='http://127.0.0.1:10801')

        except BaseException as e:
            print(e)
        finally:
            if duilie.empty():
                print(f"{n} Done")
                break


async def main():
    mk_dir('download') # 创建下载目录
    duilie = asyncio.Queue() # 创建异步队列

    url = f'http://fc2fans.club/index.php?m=content&c=index&a=lists&catid=12&page={args.page}' # 主页

    task1 = asyncio.create_task(parseLink(url, duilie)) # 解析协程
    async with aiohttp.ClientSession(trust_env=True) as session:
        task2 = [asyncio.create_task(downloader(duilie, n, session)) for n in range(16)] # 下载协程
        await asyncio.wait([task1] + task2) # 若此语句放在外面，会导致session先关闭


if __name__ == "__main__":
    asyncio.run(main())
