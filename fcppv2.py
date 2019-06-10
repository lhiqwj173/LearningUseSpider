import asyncio, aiohttp, aiofiles, os
from pyquery import PyQuery as pq

#主页
urlFormat = 'https://www.sehuatang.net/{}'

#fcppv链接
fcppv = ['https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=36&typeid=368&filter=typeid&page=%s' %i for i in range(1,51)]

#口
blowjob = ['https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=36&filter=typeid&typeid=591&page=%s' %i for i in range(1,6)]

#足
footjob = ['https://www.sehuatang.net/forum.php?mod=forumdisplay&fid=36&filter=typeid&typeid=589&page=%s' %i for i in range(1,6)]

#每日合集
allInOne = ['https://www.sehuatang.net/forum-106-%s.html' %i for i in range(1,7)]

#动漫
anime = ['https://www.sehuatang.net/forum-39-%s.html' %i for i in range(1,8)]

#国产链接
chinese = ['https://www.sehuatang.net/forum-2-%s.html' %i for i in range(1,212)]

#页面请求函数，data判定是否返回二进制数据，用以下载图片等文件
async def fetch(url, session, data=False):
    #链接可能假死或超时，捕获跳过
    try:
        async with session.get(url, proxy='http://127.0.0.1:1080') as response:
            if data:
                return await response.read()
            return await response.text()
    except:
        print("Fetch error")
#请求每一页，将目标链接放入异步队列
async def requestFirstUrl(url, duilie, session):
    htmlData = await fetch(url, session) 
    try:
        pqa = pq(htmlData)('.s.xst')
        for _ in pqa:
            fcppvLink = urlFormat.format(pq(_)('a').attr('href'))
            fcppvTitle = pq(_)('a').text()
            #由于放入操作是异步，需使用await，这里一并放入标题，方便后续使用
            await duilie.put([fcppvLink, fcppvTitle])
            #print(f'{fcppvLink}\t{fcppvTitle}')
    except:
        print("request Put error")

#请求本体页面并查找图片链接与磁力下载
async def downloadImg(duilie, session, tag):
    if not os.path.exists(f'{tag}'):
        os.mkdir(f'{tag}')
    while True:
        #异步取链接
        link = await duilie.get()
        #print(link)
        #解析页面可能为空，捕获跳出
        try:
            htmlData = await fetch(link[0], session)
            imgLink = pq(htmlData)('.zoom').attr('file')
            imgName = imgLink.split('/')[-1]
            #imgName = link[-1].split(' ')[0]
            torrentLink = pq(htmlData)('div .blockcode')('li').text()  
            print(f'{link[0]}\t{imgName}\t{torrentLink}')
        #发现经常会在此卡死，怀疑是读写出了问题，进行错误捕获处理
            async with aiofiles.open(f'{tag}/{imgName}', 'wb') as imgwriter:
                #所有异步操作都需await等待
                data = await fetch(imgLink, session, data=True)
                await imgwriter.write(data)
            async with aiofiles.open(f'{tag}/magnet.txt', 'a+') as linkwrite:
                await linkwrite.write(f'{link[-1]}\t{torrentLink}\n')
        except:
            print("Download Img Error")
        #队列为空则等于循环
        finally:
            if duilie.empty():
                break

#主函数
async def main():
    #创建队列
    number = input('请入输想要下载的数字:\n1: fc2ppv\n2: blowjob\n3: footjob\n4: allInOne\n5: anime\n6: chinese\n')
    tagDict = {'1':fcppv, '2':blowjob, '3':footjob, '4':allInOne, '5':anime, '6':chinese}
    tagDictTmp = {'1':'fcppv', '2':'blowjob', '3':'footjob', '4':'allInOne', '5':'anime', '6':'chinese'}

    #队列最大深度，超过则阻塞
    q = asyncio.Queue(maxsize=8)
    #aiohttp官方建议只开启单个session用以复用
    async with aiohttp.ClientSession() as session:
        for url in tagDict[number]:
            #创建task
            print(url)
            task1 = [asyncio.create_task(requestFirstUrl(url, q, session))]
            #8个下载协程，可自行调整，若大于队列深度则请同时调整队列最大深度
            task2 = [asyncio.create_task(downloadImg(q, session, tagDictTmp[number])) for _ in range(8)]
            await asyncio.wait(task1+task2)

asyncio.run(main())

# python3.6用户请将上方主函数注释，用下方代码

# #主函数
# async def main(loop):
#     #创建队列
#     number = input('请入输想要下载的数字:\n1: fc2ppv\n2: blowjob\n3: footjob\n4: allInOne\n5: anime\n6: chinese\n')
#     tagDict = {'1':fcppv, '2':blowjob, '3':footjob, '4':allInOne, '5':anime, '6':chinese}
#     tagDictTmp = {'1':'fcppv', '2':'blowjob', '3':'footjob', '4':'allInOne', '5':'anime', '6':'chinese'}

#     #队列最大深度，超过则阻塞
#     q = asyncio.Queue(maxsize=8)
#     #aiohttp官方建议只开启单个session用以复用
#     async with aiohttp.ClientSession() as session:
#         for url in tagDict[number]:
#             #创建task
#             print(url)
#             task1 = [loop.create_task(requestFirstUrl(url, q, session))]
#             #8个下载协程，可自行调整，若大于队列深度则请同时调整队列最大深度
#             task2 = [loop.create_task(downloadImg(q, session, tagDictTmp[number])) for _ in range(8)]
#             await asyncio.wait(task1+task2)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))

