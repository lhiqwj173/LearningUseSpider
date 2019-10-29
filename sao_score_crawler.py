# -*- coding: utf-8 -*-
# @Author: anzeme
# @Email: foxlowm@gmail.com
# @Date:   2019-10-25 20:51:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-10-29 17:57:16

import aiohttp
import asyncio
import json
import re


#首页评论，用于取得下一页cursor，可替换成任何番剧评分首页，建议运行两次，首次无法获取
start_url = 'https://bangumi.bilibili.com/review/web_api/short/list?media_id=28222723&folded=0&page_size=20&sort=0'


async def test_score(url):

    # 开启session
    async with aiohttp.ClientSession() as session:
        # 获取网页返回
        r = await session.get(url)
        # 取得json源码
        t = await r.text()
        # 转换加载json
        j = json.loads(t)

        #创建文件，将结果输入并打印一份在终端
        with open("keybord_man.txt", 'a+') as file:
            for _ in j['result']['list']:
                if _['user_rating']['score']<= 4:
                    if 'user_season' in _:
                        file.write(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t{_.get('user_season').get('last_index_show')}\n")
                        print(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t{_.get('user_season').get('last_index_show')}")
                    else:
                        file.write(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数: 未看")
                        print(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数: 未看")
        try:
            # 下一页评论的cursor会出现在当前下，将网页转换成字符形式用正则搜索即可
            c = re.findall("'cursor': '(\d+)'", str(j))[0]
            next_page = f"https://bangumi.bilibili.com/review/web_api/short/list?media_id=28222723&folded=0&page_size=20&cursor={c}"
            await test_score(next_page)
        except:
            print(url+"End")

asyncio.run(test_score(start_url))

