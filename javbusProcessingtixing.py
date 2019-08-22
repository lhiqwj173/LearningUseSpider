# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: PyCharm
# @Date: 2019/8/21 10:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08


import asyncio
from javbusProcessingfuzhuang import *

if __name__ == "__main__":
    #有码体型
    urlList = [
        "https://www.busjav.net/genre/3n",
        "https://www.busjav.net/genre/3k",
        "https://www.busjav.net/genre/2k",
        "https://www.busjav.net/genre/2i",
        "https://www.busjav.net/genre/2g",
        "https://www.busjav.net/genre/22",
        "https://www.busjav.net/genre/1t",
        "https://www.busjav.net/genre/1f",
        "https://www.busjav.net/genre/15",
        "https://www.busjav.net/genre/13",
        "https://www.busjav.net/genre/w",
        "https://www.busjav.net/genre/t",
        "https://www.busjav.net/genre/e",
    ]
    for _ in urlList:
        a = javbus()
        asyncio.run(a.Main(_))


