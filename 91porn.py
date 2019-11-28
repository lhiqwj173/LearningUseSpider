# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: vscode
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-11-28 15:56:00

from tools import *
if os.name == "posix":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parse = argparse.ArgumentParser(
     description="91pornLinkDownload not include title", prog='91porn.py')
parse.add_argument('-t', '--tag', type=str, metavar='关键字', help="example: -t 3p")
parse.add_argument('-p', '--page', metavar='页数', type=str, help="example: -p 12")
parse.add_argument('-a', '--all', action='store_true', help="下载首页全页")
parse.add_argument('--proxy', type=str, metavar='"地址:端口"', help="启用代理，暂不支持socks,example: --proxy=\"http://127.0.0.1:1080\"")
parse.add_argument('-e', '--end', type=str, metavar='结束页数', help="配合-a使用")
args = parse.parse_args()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


if args.proxy != None:
    get_html_code_proxy = partial(get_html_code, proxy=args.proxy, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, proxy=args.proxy, headers=headers)
else:
    get_html_code_proxy = partial(get_html_code, headers=headers)
    get_byte_named_proxy = partial(get_byte_named, headers=headers)

all_ready_url = []

async def crawler(url, q):
    """生产者函数，迭代解析下一页"""
    r = await get_html_code_proxy(url)
    all_ready_url.append(url)
    print("Current url: "+url)

    # 解析链接并放入异步队列

    for a in pq(r)(".video-list.row.small-up-1.medium-up-2.large-up-4")('.column'):
        await q.put([pq(a)('a').attr('href'), pq(a)('p').text().split(' ')[-1]])
        #下一页判断
    if args.all is True:
        nxtpage = pq(r)('.pagination.text-center.margin-top-4')('li').eq(-2)('a').attr('href')
        if nxtpage not in all_ready_url and nxtpage is not None and nxtpage.split("/")[-2] != str(int(args.end)+1):  # 逻辑不为空且不等于当前请求地址
           print(nxtpage)
           await crawler(nxtpage, q)

async def downloader(q, uptag):
    """消费者协程，用以下载图片，可多开"""
    while True:
        try:
            mk_dir(f"91/{uptag}")
            tmp = await q.get()
            if tmp[0] == None:
                raise TypeError('Not Link')
            l = tmp[0]
            t = tmp[-1]
            r = await get_html_code_proxy(l)

            video_url = re.findall("(http://vk.lowbb.xyz/medias/\S+)\"", r)[0]
            with open('91.txt', 'a+') as file:
                file.write(f"{video_url}\t{t}\n")
            await get_byte_named_proxy(video_url, f"./91/{uptag}/{t}.mp4")
            # with open('file.txt', 'a+') as file:
            #     file.write(f"{video_url}\n")
        except IndexError as e:
            pass
            #print(e)
        except TypeError as e:
            pass
            #print(e)
        finally:
            if q.empty():
                #print("All consumer is done, close the thread")
                break

async def Main():
    if args.tag != None:
        uptag = args.tag
        if args.page != None:
            indexHtml = f"https://91avv8.com/search/{args.tag}/page/{args.page}/"
        else:
            indexHtml = f"https://91avv8.com/search/{args.tag}/"

    else:
        uptag = '91'
        if args.page != None:
            indexHtml = f'https://91avv8.com/page/{args.page}/'
        else:
            indexHtml = 'https://91avv8.com/'
    q = asyncio.Queue(maxsize=12)

    task1 = asyncio.create_task(crawler(indexHtml, q))
    #下载协程数量一定要比一次爬取得到的资源数小，否则无法正常结束
    task2 = [asyncio.create_task(downloader(q, uptag)) for tmp in range(8)]

    await asyncio.wait([task1] + task2)

if __name__ == '__main__':
    asyncio.run(Main())
