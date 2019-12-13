# -*- coding: utf-8 -*-
# @Author: anzeme
# @Email: foxlowm@gmail.com
# @Date:   2019-10-08 01:19:20
# @Last Modified by:   anzeme
# @Last Modified time: 2019-12-13 12:06:10

import aiohttp
import os
import asyncio
import aiofiles
import re, sys, argparse, pprint, pickle
from pyquery import PyQuery as pq
from functools import partial

def mk_dir(dir):
    """目录创建函数"""
    if not os.path.exists(dir):
        os.makedirs(dir)


async def get_html_code(url, **kwargs):
    """解析函数"""
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url, proxy=kwargs.get('proxy'), headers=kwargs.get('headers'), cookies=kwargs.get('cookies'), verify_ssl=False) as response:
                    return await response.text()
    except BaseException as e:
        print(e)

# async def get_html_code(url, **kwargs):
#     """请求通常是单协程跑，所以不需要单独开一个session"""
#     return await _fetch(url, **kwargs)

async def get_byte_named(session, url, fileSavePath, **kwargs):
    """下载函数，如果关闭太快的会session会报错，单独在外层开个session调用"""
    try:
        r = await session.get(url, proxy=kwargs.get('proxy'), headers=kwargs.get('headers'), verify_ssl=False, timeout=60)
        if os.path.exists(fileSavePath):
            if str(os.path.getsize(fileSavePath)) == str(r.headers.get('Content-Length')):
                #await session.close()
                raise BaseException(f"文件已存在: {fileSavePath}")
        async with aiofiles.open("result.txt", 'a+') as file:
            await file.write(f"{url}\t{fileSavePath}\n")
        async with aiofiles.open(fileSavePath, 'wb') as file:
            while True:
                chunk = await r.content.read(2048)
                if not chunk:
                    print(fileSavePath+" Done")
                    break
                await file.write(chunk)
    except asyncio.TimeoutError as e:
        print(e)
    except ConnectionRefusedError as e:
        print(e)
    except aiohttp.ClientConnectionError as e:
        print(e)
    except BaseException as e:
        print(e)
