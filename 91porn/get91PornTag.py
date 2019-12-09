# -*- coding: utf-8 -*-
# @Author: anzeme
# @Email: foxlowm@gmail.com
# @Date:   2019-12-09 15:09:39
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-09 15:59:01


from tools import *
import pickle

d = {}
async def main():
    r = await get_html_code('https://91avv8.com/tags/', proxy='http://127.0.0.1:10801')
    # print(r)
    for _ in pq(r)('#main.large-9.medium-9.columns')('a'):
        d.setdefault(pq(_).text(), pq(_).attr('href'))

    with open('91pornTags', 'wb') as file:
        pickle.dump(d, file)
asyncio.run(main())

