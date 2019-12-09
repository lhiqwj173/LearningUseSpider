import aiohttp
import os
import asyncio
import aiofiles
import re, sys, argparse
from pyquery import PyQuery as pq
from functools import partial

def mk_dir(dir):
    """目录创建函数"""
    if not os.path.exists(dir):
        os.makedirs(dir)


async def _fetch(url, **kwargs):
    """解析函数"""
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url, proxy=kwargs.get('proxy'), headers=kwargs.get('headers'), cookies=kwargs.get('cookies'), verify_ssl=False) as response:
                if kwargs.get('data') == True:
                    return await response.read()
                else:
                    return await response.text()
    except BaseException as e:
        print(e)

async def get_html_code(url, **kwargs):
    return await _fetch(url, **kwargs)

async def get_byte(url, **kwargs):
    return await _fetch(url, data=True, **kwargs)

async def get_byte_named(session, url, filepath, **kwargs):
    try:
        r = await session.get(url, proxy=kwargs.get('proxy'), headers=kwargs.get('headers'), verify_ssl=False, timeout=60)
        if os.path.exists(filepath):
            if str(os.path.getsize(filepath)) == str(r.headers.get('Content-Length')):
                #await session.close()
                raise BaseException(f"文件已存在: {filepath}")
        async with aiofiles.open("result.txt", 'a+') as file:
            await file.write(f"{url}\t{filepath}\n")
        async with aiofiles.open(filepath, 'wb') as file:
            while True:
                chunk = await r.content.read(2048)
                if not chunk:
                    print(filepath+" Done")
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
