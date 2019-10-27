# -*- coding: utf-8 -*-
# @Author: anzeme
# @Email: foxlowm@gmail.com
# @Date:   2019-10-25 20:51:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-10-27 16:14:43

import aiohttp
import asyncio
import json
import re

#score_list = []

#with open('report.txt') as file:
#        score_list = [ _ for _ in file.readlines()]

#首页评论，用于取得下一页cursor
start_url = 'https://bangumi.bilibili.com/review/web_api/short/list?media_id=28222723&folded=0&page_size=20&sort=0'

async def test_score(url):
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        t = await r.text()
        j = json.loads(t)
        with open("keybord_man.txt", 'a+') as file:
            for _ in j['result']['list']:
                if _['user_rating']['score']<= 4:
                    if 'user_season' in _:
                        file.write(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t{_.get('user_season').get('last_index_show')}\n")
                        #print(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t{_.get('user_season').get('last_index_show')}")
                    else:
                        file.write(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数: 未看")
                        #print(f"id:{_.get('author').get('uname')}\tuid:{_.get('author').get('mid')}\t评论:{_.get('content')}\t分数:{_.get('user_rating').get('score')}\t看到集数: 未看")
        try:
            c = re.findall("'cursor': '(\d+)'", str(j))[0]
            next_page = f"https://bangumi.bilibili.com/review/web_api/short/list?media_id=28222723&folded=0&page_size=20&cursor={c}"
            await test_score(next_page)
        except:
            print(url+"End")

asyncio.run(test_score(start_url))

