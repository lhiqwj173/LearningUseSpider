import aiohttp
import os
import aiofiles
import asyncio


proxy = 'http://127.0.0.1:1080'

def mkDir(dir):
    """目录创建函数"""
    if not os.path.exists(dir):
        os.makedirs(dir)

async def fetch(url, **kwargs):
    """解析函数"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy, headers=kwargs.get('headers'), cookies=kwargs.get('cookies'), verify_ssl=False) as response:
                if kwargs.get('data') == True:
                    return await response.read()
                else:
                    return await response.text()
    except asyncio.TimeoutError:
        print("Timeout")
    except ConnectionRefusedError:
        print("ConnectionRefused")
    except:
        pass

async def getHtmlCode(url, **kwargs):
    return await fetch(url, **kwargs)

async def getByte(url):
    return await fetch(url, data=True)