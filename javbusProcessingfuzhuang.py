# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: PyCharm
# @Date: 2019/8/21 10:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08


import asyncio, aiofiles
import os
import pickle
from pyquery import PyQuery as pq
from tools import Web

with open("AllTags.txt", 'rb') as file:
    dictTag = pickle.load(file)

class javbus(object):

    def __init__(self):
        self.dictTag = dictTag
        self.cookies = {
                       "__cfduid": "d00908d789c4ace727d36a6249928efa31565789625",
                       "PHPSESSID": "5jd5625obsa8d45jhud5c81762",
                       "existmag": "all",
                          }
    @classmethod
    async def Producter(self,url, q):
        """生产者函数，迭代解析下一页"""
        w = Web(url, cookies=self.cookies)

        htmlCode = await w.getHtmlCode()
        # 解析链接并放入异步队列
        for a in pq(htmlCode)('a.movie-box'):
            await q.put(pq(a).attr('href'))

        # 下一页判断
        try:
            nxtpage = "https://www.busjav.net"+pq(htmlCode)('a#next').attr('href')
            if nxtpage != url:  # 逻辑不为空且不等于当前请求地址
                #print(nxtpage)
                await self.Producter(nxtpage, q)
        except TypeError:
            print(url+"\tLast Page")

    @classmethod
    async def Producter2(self, q, q2):
        while True:
            try:
                boxItem = await q.get()
                w2 = Web(boxItem)

                htmlCode = await w2.getHtmlCode()
                for _ in pq(htmlCode)('a.bigImage'):
                    await q2.put([boxItem,pq(_).attr('href')])
            except:
                pass
            finally:
                if q.empty():
                    break
    
    @classmethod
    async def Consumer(self, q2, url):
        """消费者协程，用以下载图片，可多开"""
        while True:
            try:
                imgUrl = await q2.get()
                w3 = Web(imgUrl[1])
                tag = url.split('/')[-1]
                typeMa = url.split('/')[3]
                dirName = f"javbus/{typeMa}/{self.dictTag[typeMa][tag]}"
                Web.mkDir(dirName)

                data = await w3.getByte()
                imgName = f"{dirName}/{imgUrl[0].split('/')[-1]}.jpg"
                print(imgName)
                
                if not os.path.exists(imgName):
                    async with aiofiles.open(imgName, 'wb') as f:
                        await f.write(data)
                else:
                    continue
            except:
                pass
            finally:
                if q2.empty():
                    break

    async def Main(self, url):
        q = asyncio.Queue()
        q2 = asyncio.Queue()

        task1 = [asyncio.create_task(self.Producter(url, q))]
        task2 = [asyncio.create_task(self.Producter2(q, q2)) for _ in range(72)]
        task3 = [asyncio.create_task(self.Consumer(q2, url)) for tmp in range(72)]

        await asyncio.wait(task1 + task3 + task2)


if __name__ == "__main__":
    #有码服装
    urlList = [
        "https://www.busjav.net/genre/9",
        "https://www.busjav.net/genre/8",
        "https://www.busjav.net/genre/1",
        "https://www.busjav.net/genre/6b",
        "https://www.busjav.net/genre/5x",
    ]
    for _ in urlList:
        a = javbus()
        asyncio.run(a.Main(_))
