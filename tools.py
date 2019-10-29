import aiohttp
import os
import asyncio

def mk_dir(dir):
    """目录创建函数"""
    if not os.path.exists(dir):
        os.makedirs(dir)

async def _fetch(url, **kwargs):
    """解析函数"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url,proxy=kwargs.get('proxy'), headers=kwargs.get('headers'), cookies=kwargs.get('cookies'), verify_ssl=False) as response:
                if kwargs.get('data') == True:
                    return await response.read()
                else:
                    return await response.text()
    except asyncio.TimeoutError:
        print("Timeout")
    except ConnectionRefusedError:
        print("ConnectionRefused")
    except:
        print("Unknow Error")

async def get_html_code(url, **kwargs):
    return await _fetch(url, **kwargs)

async def get_byte(url, **kwargs):
    return await _fetch(url, data=True, **kwargs)