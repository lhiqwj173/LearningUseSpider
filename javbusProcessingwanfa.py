# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: PyCharm
# @Date: 2019/8/21 10:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08


import asyncio
from javbusProcessingfuzhuang import *

if __name__ == "__main__":
    #有码玩法
    urlList = [
        "https://www.busjav.net/genre/51",
        "https://www.busjav.net/genre/4f",
        "https://www.busjav.net/genre/4c",
        "https://www.busjav.net/genre/4b",
        "https://www.busjav.net/genre/3z",
        "https://www.busjav.net/genre/3y",
        "https://www.busjav.net/genre/3s",
        "https://www.busjav.net/genre/3p",
        "https://www.busjav.net/genre/3m",
        "https://www.busjav.net/genre/3h",
        "https://www.busjav.net/genre/36",
        "https://www.busjav.net/genre/2u",
        "https://www.busjav.net/genre/25",
        "https://www.busjav.net/genre/1q",
        "https://www.busjav.net/genre/1m",
        "https://www.busjav.net/genre/1l",
        "https://www.busjav.net/genre/1h",
        "https://www.busjav.net/genre/1b",
        "https://www.busjav.net/genre/1a",
        "https://www.busjav.net/genre/14",
        "https://www.busjav.net/genre/q",
        "https://www.busjav.net/genre/d",
        "https://www.busjav.net/genre/6",
        "https://www.busjav.net/genre/3",
        "https://www.busjav.net/genre/5m",
        "https://www.busjav.net/genre/5y",
        "https://www.busjav.net/genre/63",
    ]

    for _ in urlList:
        asyncio.run(Main(_))
