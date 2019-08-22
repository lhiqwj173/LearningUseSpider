# -*- coding: utf-8 -*-
# @Author: anzeme
# @Software: PyCharm
# @Date: 2019/8/21 10:38
# @Last Modified by:   anzeme
# @Last Modified time: 2019-07-02 星期三 22:08


import asyncio
from javbusProcessingfuzhuang import javbus

if __name__ == "__main__":
    #有码行为
    urlList = [
        "https://www.busjav.net/genre/4w",
        "https://www.busjav.net/genre/4t",
        "https://www.busjav.net/genre/4j",
        "https://www.busjav.net/genre/47",
        "https://www.busjav.net/genre/46",
        "https://www.busjav.net/genre/45",
        "https://www.busjav.net/genre/42",
        "https://www.busjav.net/genre/3q",
        "https://www.busjav.net/genre/3l",
        "https://www.busjav.net/genre/3f",
        "https://www.busjav.net/genre/2h",
        "https://www.busjav.net/genre/24",
        "https://www.busjav.net/genre/1z",
        "https://www.busjav.net/genre/1s",
        "https://www.busjav.net/genre/1r",
        "https://www.busjav.net/genre/1p",
        "https://www.busjav.net/genre/1o",
        "https://www.busjav.net/genre/1j",
        "https://www.busjav.net/genre/19",
        "https://www.busjav.net/genre/x",
        "https://www.busjav.net/genre/u",
        "https://www.busjav.net/genre/r",
        "https://www.busjav.net/genre/n",
        "https://www.busjav.net/genre/h",
        "https://www.busjav.net/genre/5",
        "https://www.busjav.net/genre/4",
        "https://www.busjav.net/genre/6m",
    ]

    for _ in urlList:
        a = javbus()
        asyncio.run(a.Main(_))
