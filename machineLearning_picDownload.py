#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# @Author: Anzeme
# @Email:  foxlowm@gmail.com
# @Date:   2018-12-12 18:33:21
# @Last Modified by:   jackyao
# @Last Modified time: 2018-12-21 16:10:29

import os, asyncio, aiohttp, aiofiles, json
from urllib.parse import quote
from pyquery import PyQuery as pq
from multiprocessing import Process


"""Linux平台可用uvloop事件处理，速度比肩go"""
#if os.name == 'posix':
#    import uvloop
#    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


keyword=['飞机', '手机', '鸟', '猫', '狗', '青蛙', '马', '船', '卡车', '鹿']
link = []

"""生成json链接"""
def genurl(keyword):
    """根据关键字创建目录"""
    for _ in keyword:
        if not os.path.exists(_):
            os.mkdir(_)
        """编码url关键字"""
        keyw = quote(_)
        headurl = f'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={keyw}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word={keyw}&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&expermode=&selected_tags=&pn='
        url2 = ['%s&rn=30' %i for i in range(301) if i%30 == 0]
        """生成url"""
        for _ in url2:
            link.append(headurl+_)


genurl(keyword)
eachPartlen = len(link)//8

newLinkList = [ link[i:i+eachPartlen] for i in range(0, len(link), eachPartlen)]

"""队列"""

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

async def getImg(url, sess, q):
    async with sess.get(url) as res:
        try:
            html = await res.text()
            """json数据类型，取得名称和链接为下载与目录做准备"""
            j = json.loads(html)
            for _ in j['data']:
                    imgurl = _['middleURL']
                    d = j['queryExt']
                    #print('Put Link {}\t{}'.format(imgurl, d))
                    await q.put([imgurl, d])
        except KeyError:
            print("Error Link, Pass")
        except UnicodeDecodeError:
            print("Url Reqest Error, Pass")
        except:
            print("Unkown Error, Pass")


async def downloadImg(s, q):
    while True:
        try:
            tmp = await q.get()
            print("Get {}".format(tmp[0]))
            async with s.get(tmp[0], headers=headers) as res:
                data = await res.read()
            async with aiofiles.open('./{}/{}'.format(tmp[1], tmp[0].split('/')[-1]), 'wb') as aiof:
                await aiof.write(data)
        except OSError:
            print("无法创建文件名")
            continue
        except:
            print("服务器断开连接，建议降低协程数")
            continue
        finally:
            if q.empty():
                break

async def main(partLink):
    q = asyncio.Queue(maxsize=64)
    async with aiohttp.ClientSession() as session:
        """开启8个协程与N个协程"""
        d = [asyncio.create_task(downloadImg(session, q)) for _ in range(8)]
        g = [asyncio.create_task(getImg(l, session, q)) for l in partLink]

        await asyncio.wait(g+d)


def multiMain(pLink):
    asyncio.run(main(pLink))

if __name__ == '__main__':
    p = [Process(target=multiMain, args=(p,)) for p in newLinkList]
    for _ in p:
        _.start()
    for _ in p:
        _.join()
