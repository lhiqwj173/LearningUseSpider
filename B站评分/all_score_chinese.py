# -*- coding: utf-8 -*-
# @Author: anzeme
# @Email: foxlowm@gmail.com
# @Date:   2019-10-25 20:51:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-13 12:47:37

import aiohttp,os,asyncio,aiofiles
from multiprocessing import Pool
import pickle
if os.name == "posix":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#import torch.multiprocessing
#torch.multiprocessing.set_sharing_strategy('file_system')

# 国产番剧ID与名称
with open('bangumi_id_name_chinese', 'rb') as file:
    bangumi_id_name_chinese = pickle.load(file)


async def test_score(k, v, u=None):
    url = f"https://bangumi.bilibili.com/review/web_api/short/list?media_id={k}&folded=0&page_size=30&sort=0"
    # 开启session
    async with aiohttp.ClientSession() as session:
        # 获取网页返回
        if u is not None:
            r = await session.get(u)
        else:
            r = await session.get(url)

        # 取得json源码
        t = await r.json()
        for _ in t['result']['list']:
            try:
                if _['user_rating']['score'] <= 2:
                    async with aiofiles.open("allresult_chinese_lowTo2_eight.txt", 'a+', encoding='utf-8') as file:
                        if 'user_season' in _:
                            #file.write(f"{_.get('author').get('mid')}\n")
                            #if str(_.get('author').get('mid')) in all_uid:
                            await file.write(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数:{_.get('user_season').get('last_ep_index')}\t{v}\n")
                            #print(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数:{_.get('user_season').get('last_ep_index')}\t{v}")
                        else:
                            #if str(_.get('author').get('uname')) in all_uid:
                            await file.write(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数: 未看\t{v}\n")
                            #print(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数: 未看\t{v}")
            except KeyError as e:
                print(f"{e}\t{v}")
            except:
                pass
                # 下一页评论的cursor会出现在当前下，将网页转换成字符形式用正则搜索即可
        try:
            c = t['result']['list'][29]['cursor']
            # c = re.findall("\'cursor\': \'(\d+)\'", str(t))[0]
            next_page = f"https://bangumi.bilibili.com/review/web_api/short/list?media_id={k}&folded=0&page_size=30&cursor={c}"
            # print(next_page)
            await test_score(k, v, u=next_page)
        except:
            print(f"End\t{u}\t{v}")

async def main(pack):   

    task = [asyncio.create_task(test_score(k, v)) for k,v in pack]

    await asyncio.wait(task)


def main_main(a):
    asyncio.run(main(a))

if __name__ == "__main__":
    # asyncio.run(main())
    a = [ [k,v] for k,v in bangumi_id_name_chinese.items() ]
    b = [ a[i:i+4] for i in range(0, len(a), 4)]
    p = Pool(2)
    p.map(main_main, b)
        

    # tmp = 0
    # p = [Process(target=main, args=(k, v)) for k,v in bangumi_id_name_chinese.items()] 
    # for _ in p:
    #     _.start()
    #     tmp += 1
    #     if tmp % 8 == 0:
    #         _.join()
    # for k,v in bangumi_id_name_chinese.items():
    #     main(k,v)
    #     break
