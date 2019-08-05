#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# @Author: Anzeme
# @Email:  foxlowm@gmail.com
# @Date:   2018-12-12 18:33:21
# @Last Modified by:   jackyao
# @Last Modified time: 2018-12-21 16:10:29

import os, asyncio, aiohttp, aiofiles, json
from urllib.parse import quote
from multiprocessing import Process
from tools import Web

"""Linux平台可用uvloop事件处理，速度比肩go"""
# if os.name == 'posix':
#    import uvloop
#    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


keyword = ['飞机', '手机', '鸟', '猫', '狗', '青蛙', '马', '船', '卡车', '鹿']
link = []

def genurl(keyword):
    """根据关键字创建目录并添加链接"""
    for _ in keyword:
        if not os.path.exists(_):
            os.mkdir(_)

        keyw = quote(_)
        headurl = f'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={keyw}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={keyw}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&selected_tags=&pn='

        url2 = ['%s&rn=30' % i for i in range(301) if i % 30 == 0]
        for _ in url2:
            link.append(headurl+_)
genurl(keyword)

#分段，为多进程做准备
eachPartlen = len(link) // 8
newLinkList = [link[i:i + eachPartlen] for i in range(0, len(link), eachPartlen)]

headers = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'img4.imgtn.bdimg.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}


async def Producter(url, q):
    w = Web(url)
    try:
        j = json.loads(await w.getHtmlCode())
        for _ in j['data']:
            imgurl = _['middleURL']
            d = j['queryExt']
            await q.put([imgurl, d])
    except KeyError:
        pass
    except:
        pass

async def Consumer(q):
    while True:
        try:
            tmp = await q.get()
            #print("Get {}".format(tmp[0]))
            w = Web(tmp[0], headers=headers)
            print(f'./{tmp[1]}/{tmp[0].split("/")[-1]}')

            async with aiofiles.open(f'./{tmp[1]}/{tmp[0].split("/")[-1]}', 'wb') as aiof:
                await aiof.write(await w.getByte())
        except:
            continue
        finally:
            if q.empty():
                break

async def main(partLink):
    q = asyncio.Queue(maxsize=32)
    task2 = [asyncio.create_task(Consumer(q)) for _ in range(8)]
    task1 = [asyncio.create_task(Producter(l, q)) for l in partLink]

    await asyncio.wait(task1+task2)


def multiMain(pLink):
    asyncio.run(main(pLink))


if __name__ == '__main__':
    p = [Process(target=multiMain, args=(p,)) for p in newLinkList]
    for _ in p:
        _.start()
    for _ in p:
        _.join()
