import asyncio, aiohttp, aiofiles, os
from pyquery import PyQuery as pq
from multiprocessing import Process
from datetime import datetime

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
        async with session.get(url, timeout=20, proxy='http://127.0.0.1:1080', verify_ssl=False) as response:
            if data:
                return await response.read()
            return await response.text()
    except:
        print("fetch url error, maybe timeout or session closed!!!")    
        
#请求每一页，将目标链接放入异步队列
async def requestFirstUrl(url, duilie, session):
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
        nxtpage = pq(htmlData)('#fd_page_bottom')('.nxt').attr('href')
        if nxtpage is not None:
            print(f'Found next page {urlFormat.format(nxtpage)}')
            await requestFirstUrl(urlFormat.format(nxtpage), duilie, session)
      
#请求本体页面并查找图片链接与磁力下载
async def downloadImg(duilie, session, tag):
    if not os.path.exists(f'sehuatang/{tag}'):
        os.mkdir(f'sehuatang/{tag}')
    while True:
        #get接口也是协程，需await
        link = await duilie.get()
        #print(link)
        #解析页面可能为空，捕获跳出
        try:
            htmlData = await fetch(link[0], session)
            imgLink = pq(htmlData)('.zoom').attr('file')
            imgName = imgLink.split('/')[-1]
            if os.path.exists(f'sehuatang/{tag}/{imgName}'):
                print("Img exists, Pass")
                continue
            #imgName = link[-1].split(' ')[0]
            torrentLink = pq(htmlData)('div .blockcode')('li').text()  
            print(f'{link[-1]}\t{torrentLink}')
            #所有异步操作都需await等待
            async with aiofiles.open(f'sehuatang/{tag}/{imgName}', 'wb') as imgwriter:
                data = await fetch(imgLink, session, data=True)
                await imgwriter.write(data)
            async with aiofiles.open(f'sehuatang/{tag}/magnet.txt', 'a+', encoding='utf-8') as linkwrite:
                await linkwrite.write(f'{link[0]}\t{link[-1]}\t{torrentLink}\n')
        #队列为空则等于循环
        except AttributeError:
            print("Not found img Link!!!")
            continue
        except TypeError:
            print("Not data found, maybe link dead")
            continue
        except:
            print("Other error, maybe no maybe.....")
            continue
        finally:
            if duilie.empty():
                break

async def main(k, v):
    #提示用户选择
    #创建队列，并指定队列最大深度，超过则阻塞
    q = asyncio.Queue(maxsize=32)
    #aiohttp官方建议只开启单个session用以复用
    async with aiohttp.ClientSession() as session:
        #创建task
        task1 = [asyncio.create_task(requestFirstUrl(v, q, session))]
        #8个下载协程，可自行调整，若大于队列深度则请同时调整队列最大深度
        task2 = [asyncio.create_task(downloadImg(q, session, k)) for _ in range(8)]
        await asyncio.wait(task1+task2)

def m(k, v):
    asyncio.run(main(k, v))

if __name__ == '__main__':
    tagDict = {'fcppv':fcppv, 'blowjob':blowjob, 'footjob':footjob, 'allInOne':allInOne, 'anime':anime, 'chinese':chinese, 'noHorse':noHorse, 'Horse': Horse, 'japanChinese': japanChinese, 'europe': europe}
    starttime = datetime.now()
    print(f'Start at {starttime}')
    #tagDict = {'anime':anime}
    p = [Process(target=m, args=(k, v)) for k,v in tagDict.items()]
    for _ in p:
        _.start()
    for _ in p:
        _.join()
    endtime = datetime.now()
    print(f'End at {endtime}\t Spend {endtime-starttime}s')
    
