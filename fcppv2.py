#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: notepad++
# @Date: 2019-06-25 星期三 22:26
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:26

import asyncio, aiohttp, aiofiles, os
from pyquery import PyQuery as pq
from multiprocessing import Process
from datetime import datetime

#本爬虫使用生产者消费者模型，页数获取为递归方式，消费者最大连接数不超过32为宜

#主页
urlFormat = 'https://www.sehuatang.net/{}'

#无码
noHorse = 'https://www.sehuatang.net/forum-36-1.html'

#欧美
europe = 'https://www.sehuatang.net/forum-38-1.html'

#中文字幕
japanChinese = 'https://www.sehuatang.net/forum-103-1.html'

#有码
Horse = 'https://www.sehuatang.net/forum-37-1.html'

#fcppv链接
fcppv = 'https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=36&typeid=368&filter=typeid&page=1'

#口
blowjob = 'https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=36&filter=typeid&typeid=591&page=1'

#足
footjob = 'https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=36&filter=typeid&typeid=589&page=1'

#每日合集
allInOne = 'https://www.sehuatang.net/forum-106-1.html'

#动漫
anime = 'https://www.sehuatang.net/forum-39-1.html'

#国产链接
chinese = 'https://www.sehuatang.net/forum-2-1.html'

if not os.path.exists('sehuatang'):
    os.mkdir('sehuatang')

#页面请求函数，data判定是否返回二进制数据，用以下载图片等文件
async def fetch(url, session, data=False):
    #链接可能假死或超时，捕获跳过
    try:
        async with session.get(url, proxy='http://127.0.0.1:1080', verify_ssl=False) as response:
            if data:
                return await response.read()
            return await response.text()  
    except aiohttp.ClientConnectorSSLError as e:
        assert isinstance(e, ssl.SSLError)
    except:
        print("fetch url error, maybe timeout or session closed!!!")  
        
#请求每一页，将目标链接放入异步队列
async def requestFirstUrl(url, duilie, session, tag, c, e):
    htmlData = await fetch(url, session) 
    pqa = pq(htmlData)('.s.xst')
    try:
        for _ in pqa:
            fcppvLink = urlFormat.format(pq(_)('a').attr('href'))
            fcppvTitle = pq(_)('a').text()
            #由于放入操作是异步，需使用await，这里一并放入标题，方便后续使用
            await duilie.put([fcppvLink, fcppvTitle])
            #print(f'{fcppvLink}\t{fcppvTitle}')            
    except:
        print("Maybe not a url link, Pass")
    finally:
    #寻找下一页按扭，存在便迭代自已存入链接，需下载全部内容的请去除注释
        if e < c:
            e += 1
            nxtpage = pq(htmlData)('#fd_page_bottom')('.nxt').attr('href')
            if nxtpage is not None:
                print(f'Found next page {tag}\t{urlFormat.format(nxtpage)}')
                await requestFirstUrl(urlFormat.format(nxtpage), duilie, session, tag, c, e)
        
#请求本体页面并查找图片链接与磁力下载
async def downloadImg(duilie, session, tag):
    if not os.path.exists(f'sehuatang/{tag}'):
        os.mkdir(f'sehuatang/{tag}')
    while True:
        #get也是异步操作，需await
        link = await duilie.get()
        #print(link)
        #解析页面可能为空，捕获跳出
        try:
            htmlData = await fetch(link[0], session)
            imgLink = pq(htmlData)('.zoom')
            torrentLink = pq(htmlData)('div .blockcode')('li').text() 
            async with aiofiles.open(f'sehuatang/{tag}/magnet.txt', 'a+', encoding='utf-8') as linkwrite:
                await linkwrite.write(f'{link[0]}\t{link[-1]}\t{torrentLink}\n')
            for _ in imgLink:
                iname = pq(_).attr('file')
                imgName = iname.split('/')[-1]
                #if os.path.exists(f'sehuatang/{tag}/{imgName}'):
                #print("Img exists, Pass")
                #    continue
            #imgName = link[-1].split(' ')[0]
            #print(f'{link[-1]}\t{torrentLink}')
            #所有异步操作都需await等待
                with open(f'sehuatang/{tag}/{link[-1].split(" ")[0]}_{imgName}', 'wb') as imgwriter:
                    data = await fetch(iname, session, data=True)
                    imgwriter.write(data)
        #队列为空则等于循环
        except AttributeError:
            #print("Not found img Link!!!")
            continue
        except TypeError:
            print("Not data found, maybe link dead")
            continue
        except:
            print("Other error, maybe no maybe.....")
            continue
        finally:
            if duilie.empty():
                print(f"{tag} Task is Done !!!!!!!")
                break

async def main(k, v):
    #提示用户选择
    #创建队列，并指定队列最大深度，超过则阻塞
    q = asyncio.Queue(maxsize=128)
    tmp = 2
    e = 1
    #aiohttp官方建议只开启单个session用以复用
    async with aiohttp.ClientSession() as session:
        #创建task
        task1 = [asyncio.create_task(requestFirstUrl(v, q, session, k, tmp, e))]
        #8个下载协程，可自行调整，若大于队列深度则请同时调整队列最大深度
        task2 = [asyncio.create_task(downloadImg(q, session, k)) for _ in range(4)]
        await asyncio.wait(task1+task2)

def m(k, v):
    asyncio.run(main(k, v))

if __name__ == '__main__':
    tagDict = {'fcppv':fcppv, 'blowjob':blowjob, 'footjob':footjob, 'allInOne':allInOne, 'anime':anime, 'chinese':chinese, 'noHorse':noHorse, 'Horse': Horse, 'japanChinese': japanChinese, 'europe': europe}
    #tagDict = {'fcppv':fcppv, 'blowjob':blowjob, 'footjob':footjob, 'allInOne':allInOne, 'anime':anime, 'chinese':chinese, 'noHorse':noHorse, 'Horse': Horse, 'europe': europe}
    #tagDict = {'japanChinese': japanChinese}
    #计时开始
    starttime = datetime.now()
    #print(f'Start at {starttime}')
    #tagDict = {'anime':anime}
    #创建进程
    p = [Process(target=m, args=(k, v)) for k,v in tagDict.items()]
    #开始进程
    for _ in p:
        _.start()
    #阻塞进程，为的是下面计算时间
    for _ in p:
        _.join()
    endtime = datetime.now()
    print(f'Start at {starttime}\tEnd at {endtime}\t Spend {endtime-starttime}s')
    
